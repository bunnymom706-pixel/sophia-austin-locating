# MARKETPLACE ENGINE: 20 INBOUND MESSAGES A DAY
Handoff brief for a browser-connected Claude Code session.
Operator: Sophia Reddehase, Spirit Real Estate Group, TREC #831516. Austin metro apartment locator.
Repo: bunnymom706-pixel/sophia-austin-locating

---

## 0. READ THIS FIRST, AGENT

You are running a posting engine, not writing one ad. Your job each session:
keep a rotating inventory of live Facebook Marketplace rental listings large enough
to produce 20 inbound Messenger conversations per day, without getting any account
flagged again.

**Load the skill `apartment-marketplace-ads` before writing any ad copy.** The locked
format, emoji rules, compliance rules, and signature live there and in
`templates/spirit_marketplace_ad_script.md`. Do not invent a new format.

**Never publish. Always save as draft.** Sophia hits publish herself. This is a hard rule
from the existing skill and it stays.

**Prior state:** an earlier account was throttled/restricted for posting near-identical ads
in bursts. Everything in Section 2 exists because of that. Treat account health as the
binding constraint, not volume.

---

## 1. THE MATH (why 20/day is a volume problem, not a copy problem)

Observed Marketplace rental behavior in a metro like Austin:

| | |
|---|---|
| Fresh listing, first 24h | ~1.5 to 3 messages |
| Same listing, day 2-3 | ~0.5 to 1/day |
| Same listing, day 4+ | ~0.1 to 0.3/day, decays to 0 |
| Listing lifespan before dead | 5 to 7 days |

To hold 20/day you need **both**:

- **Fresh flow:** 8 to 12 new or renewed listings posted per day
- **Standing inventory:** 45 to 60 listings live at once, trickling

Spread across 3 accounts that is **3 to 4 fresh posts per account per day**. That is
under every throttle threshold. 12 ads in one hour on one account is what killed the last one.

### Where the inventory comes from

Sophia has ~22 named properties with photos in `assets/properties/` plus 7 generic ZIP photo
sets. That looks like 29 listings. It is actually 90+.

**Each floorplan is a legitimately distinct listing.** One property = studio + 1bd + 2bd + 3bd
= up to 4 real listings, different price, different photos, different title, different slogan.
This is the single biggest unlock and it is not duplicate posting: different unit, different
price, different ad.

`22 properties x ~3 floorplans = ~66 base listings`
`+ 7 generic ZIP sets x 3 = ~21`
`= ~87 listing slots, cycling on a 6-day rotation`

That produces the fresh flow without ever reposting the same ad twice in a week.

---

## 2. ACCOUNT HEALTH PROTOCOL (non-negotiable, this is why she got throttled)

Facebook flags on: image hash collisions, text similarity, posting velocity, contact info
in body, and category mismatch. Fix all five.

### 2a. Photo de-duplication
Marketplace hashes images. The same JPG on two listings reads as duplicate posting even
when the ads are different. Before any photo is used a second time, vary it:

```bash
# per listing, generate a varied copy of each photo
convert input.jpg -rotate 0.4 -crop 98%x98%+0+0 +repage \
  -modulate 100,101,100 -quality 92 output.jpg
```
Vary the rotate value (0.3 to 0.8, alternate sign), crop percent (97-99), and modulate
saturation (99-102) per listing so no two derived files share a hash. These are Sophia's
own licensed marketing photos; this is collision avoidance on her own assets, not disguise.

**Never reuse the exact same file across two live listings.** Never reuse the same *lead
photo* (first image) across any two listings at all, varied or not.

### 2b. Text variation
- Slogan: unique per ad, never repeated. Ever.
- Service intro: rotate the 3 variants in the script, plus write new ones.
- CTA: rotate the 3 variants.
- Never paste an ad body that shares more than ~40% of its sentences with a live ad.

### 2c. Velocity
| Account age | Max posts/day | Spacing |
|---|---|---|
| Week 1 (new/recovering) | 2 | 4+ hours apart |
| Week 2 | 3 | 3+ hours apart |
| Week 3+ | 4 to 5 | 2+ hours apart, never 2 in the same 60 min |

Post in the windows that match renter behavior: **7-9am, 12-1pm, 5-7pm, 9-10pm CT.**
Never post a batch at 2am.

### 2d. Hard nevers (already in the script, repeated because they are also flag triggers)
- No phone, no email, no link, no "text me." Messenger only.
- No property name, no cross street, no address in the published body.
- No fair housing language, no crime/safety language.
- Correct category: Housing > Apartment for rent. Only fall back to another category if
  Housing is unavailable on that account.
- Price in the body must equal the price field to the dollar.

### 2e. Renewal, not repost
Marketplace's built-in "Renew listing" is safe. Deleting and re-posting the same listing
is a duplicate-content flag. Renew on day 4. Delete and rebuild fresh from a different
floorplan on day 7.

---

## 3. STEP ONE FOR THE AGENT: BUILD THE MANIFEST

Photos are loosely organized. Before posting anything, build
`playbooks/property_manifest.csv` from `assets/properties/` with these columns:

```
property_key,display_area,zip,photo_files,floorplans,base_rent_low,management_co,is_greystar_or_rpm,special,special_term,pet_policy,standout_feature,last_posted,account_used,status
```

Rules:
- One row per **property + floorplan**, not per property. That is the listing unit.
- `display_area` is the neighborhood phrasing that goes in the header (e.g. "Northwest Austin").
- `photo_files` = 4 to 8 files, lead photo listed first, no file shared as a lead with another row.
- Leave `base_rent_low`, `special`, `pet_policy` blank until confirmed. **Never invent a price
  or a special.** Pull from the apartments.com link or ask Sophia.
- `last_posted` and `account_used` drive the rotation. Update them after every draft.

Ignore these files when building it: anything matching
`General_Austin_Properties_*`, `Market_Costar_*`, `*blobtest*`, `*test-square*`,
`*screenshot*`, `*Snapseed*`, `*signature*`, `*brand*`, `*ad_view*`, and the keyboard-mash
filenames. Those are brand assets and scratch, not property photos.

Known property keys already in the repo:
`Trails_At_Canyon_Creek, Water_Oak, The_Prado_ATX, The_Bower, Presidium_183, Pearl_Bee_Cave,
Oasis_at_Round_Rock, Museo_at_Channing_Marks, Jolie_Pflugerville, Ivy_Heights,
Hillside_on_Parmer, Broadstone_North_ATX, Alara_North_Burnet, The_Bond_Austin,
The_Axel_Austin, Casa_Agave_Austin, Bridge_At_South_Point, Arden_At_Kohlers_Crossing,
Flats_At_San_Felipe`
Generic ZIP sets: `78753, 78747, 78744, 78738, 78721, 78717, 78664`

---

## 4. THE DAILY RUN

Each session, in order:

1. **Read** `property_manifest.csv`. Select rows where `last_posted` is null or 6+ days old.
2. **Pick 9 to 12** for today, spread so no two from the same property go up on the same
   account on the same day.
3. **Assign accounts** round-robin, respecting each account's daily cap from 2c.
4. **Confirm pricing.** If `base_rent_low` is blank or older than 7 days, ask Sophia for the
   apartments.com link or the current number. Do not draft a listing with a guessed price.
5. **Vary photos** per 2a into `build/<date>/<property_key>_<floorplan>/`.
6. **Write the ad** using the locked format from the skill. New slogan every time.
7. **Drive the browser**: create the Marketplace listing, upload varied photos, fill title,
   price, category, description. **Save as draft.**
8. **Update the manifest**: `last_posted`, `account_used`, `status=draft`.
9. **Report to Sophia**: a numbered list of drafts ready to publish, with the publish window
   for each (from 2c), so she can space them.

### Title formula
`[Beds] Bed [Baths] Bath [Area] - [Special or Standout] - $[PRICE]`

Vary the area phrasing across listings of the same property: "Northwest Austin", "78729",
"Near the Domain", "North Austin". Marketplace search is location-keyword driven and this
widens coverage without duplicating.

### Price ladder
Post the **lowest available floorplan price** as the listing price. The 2bd listing prices at
the 2bd low. Never a net effective number, never a blended number. Base rent only, special
stated separately as "on top of base rent" with its minimum term.

---

## 5. CONVERSION: SPEED-TO-LEAD AND THE REPLY LADDER

Right now Sophia replies manually with no system. Twenty messages a day without a system
is twenty leaks. Build `playbooks/reply_ladder.md` with these, and set them up as Messenger
saved replies.

**Speed target: first reply inside 5 minutes.** Marketplace renters message 6 to 10 locators
at once. First substantive reply wins the majority of them. This matters more than ad volume
once volume exists.

### R1 - instant, to every single message
> Hi! Yes that one's still available. Quick so I can pull the right numbers for you: what's
> your move-in month, your budget, and how many bedrooms? I work the whole Austin metro so
> if this one doesn't fit I'll find the one that does.

### R2 - after they answer, qualify
Get, in one message, not an interrogation: move-in date, budget ceiling, beds, pets,
work/commute anchor, and anything that will show up on a screening anyway (credit range,
income, voucher, visa-only, broken lease, co-signer). That last part goes straight into the
FILE NOTES block of the guest card so nothing blows up at application.

### R3 - deliver value before asking for anything
Send 2 to 3 real options with real numbers. Not a list of names. This is where a locator
wins: everyone else sends links, she sends confirmed pricing.

### R4 - TREC compliance
After the first substantive Messenger reply, send the TREC Information About Brokerage
Services link in that thread. This is in the existing script and it is a license obligation,
not an option. The disclosures page in this repo has it.

### R5 - handoff to the guest card
Once they pick a property, switch to `templates/spirit_guest_card_script.md`, send from
`Sophia.reddehase@spiritre.com`, log in clientmgr.us same day.

### R6 - no reply after 24h
> Still looking, or did you land somewhere? Either answer is fine, I just don't want to
> keep a unit on hold for you if you're set.

### R7 - dead lead, 7 days
Move to the deal-drop list. Do not delete. Austin leases turn over; they rent again.

---

## 6. TRACKING

`playbooks/lead_log.csv`:
```
date,listing_property,listing_floorplan,account,first_msg_time,first_reply_time,name,budget,beds,movein,stage,property_registered,card_sent_date,outcome
```

Two numbers Sophia should see weekly:
- **Messages per listing** by property. Kill the bottom third, double the top third's floorplan coverage.
- **Median speed-to-lead.** If it climbs past 10 minutes, volume is outrunning capacity and
  the fix is a faster R1, not more ads.

---

## 7. RAMP SCHEDULE

Account is recovering from a restriction. Do not open at full volume.

| Week | Posts/day/account | Accounts | Live inventory | Expected msgs/day |
|---|---|---|---|---|
| 1 | 2 | 3 | ~18 | 4 to 7 |
| 2 | 3 | 3 | ~35 | 8 to 12 |
| 3 | 4 | 3 | ~50 | 14 to 18 |
| 4+ | 4 to 5 | 3 | 55 to 65 | **20 to 28** |

If any account gets a warning, a listing removal, or a reach drop: **that account goes to
zero posts for 72 hours**, the other two hold steady, and the removed listing's copy and
photos get retired permanently. Do not appeal and repost the same thing.

---

## 8. WHAT SUCCESS LOOKS LIKE BY WEEK 4

- ~87 manifest rows, 55 to 65 live at any moment, 6-day rotation
- 12 fresh drafts queued per day across 3 accounts, spaced into the 4 posting windows
- Median first reply under 5 minutes
- Every message logged, every chosen property guest-carded same day
- Zero flagged listings for 30 straight days

Volume is the input. The account surviving is the constraint. Do not trade the second for the first.

---

## 9. AGENT CHECKLIST, EVERY SINGLE DRAFT

- [ ] Loaded the `apartment-marketplace-ads` skill for the format
- [ ] Price confirmed from a real source, not inferred
- [ ] Address line deleted from the body
- [ ] Price in body equals price field to the dollar
- [ ] Slogan unique, never used before
- [ ] Intro and CTA different from the last 3 ads on this account
- [ ] 3 emoji max, none in the slogan, none repeated, paw only on pets
- [ ] No em dashes
- [ ] No phone, email, link, property name, or cross street
- [ ] Special says "on top of base rent" and names the minimum term
- [ ] Signature reads "Spirit Real Estate Group" (no LLC), TREC #831516
- [ ] Photos varied, lead photo not used on any other live listing
- [ ] Saved as **draft**, not published
- [ ] Manifest row updated
