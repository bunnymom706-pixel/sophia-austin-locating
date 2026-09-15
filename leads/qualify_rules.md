# Lead qualification rubric (Craigslist Austin, housing wanted)

Sophia is a licensed apartment locator (Spirit Real Estate Group, TREC #831516). She is paid by apartment communities, never by renters. A lead is worth her time only if the poster will likely lease at a managed apartment community in the Austin metro.

Score each post 0 to 100. Start at 50, apply every line that fits, clamp to 0..100.

## Add
- +20 budget >= $1,100/mo stated or clearly implied (community-level rent)
- +10 budget >= $1,600/mo
- +15 move-in within 90 days (stated date, "ASAP", "next month", "by Nov 1")
- +15 wants an apartment/condo/townhome unit (not a whole house, land, trailer, or a room in someone's home)
- +10 Austin metro: Austin zips 787xx, Cedar Park, Round Rock, Pflugerville, Georgetown, Leander, Kyle, Buda, Hutto, Manor
- +10 relocating from out of state or out of city (job, school, military, "moving to Austin")
- +10 mentions credit issues, past eviction, broken lease, no rental history, low score, "second chance" (Sophia's niche: she knows which communities approve)
- +5 leaves a direct email or phone in the post (faster contact than the relay)
- +5 posted within the last 24 hours
- +5 lease term 6 to 15 months

## Subtract
- -40 is a landlord, agent, locator, property manager, or company advertising (not a renter)
- -30 wants a room, roommate, couch, shared space, or sublet under 3 months
- -25 budget under $800/mo
- -25 wants a house with acreage, RV/trailer spot, or outside the metro (San Antonio, Dallas, Houston, Killeen only)
- -20 scam signals: wire money, overseas, "God bless" + urgency, asks for deposit, copy-paste template, wrong city
- -15 needs Section 8 / voucher only (few luxury communities accept; still B-tier if budget fits)
- -10 post older than 3 days
- -10 no budget and no timeline at all

## Tier
- A: score >= 70. Sophia contacts first thing.
- B: 40 to 69. Worth one reply.
- C: < 40. Drop from digest, keep in JSON.

## Output per lead
`{pid, section, score, tier, budget, timeline, area, beds, why (1 line), red_flags (list), contact: {reply_email, emails_in_post, phones_in_post}, reply_draft}`
Budget/timeline/area/beds: pull from text, "unknown" if absent. Never invent facts.
