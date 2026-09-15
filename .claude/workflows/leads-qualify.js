export const meta = {
  name: 'leads-qualify',
  description: 'Qualify, score, and draft replies for tonight\'s Craigslist wanted-post leads, then rank them',
  whenToUse: 'After leads/harvest.py has written a nightly JSON. args = {nightFile, pids, chunk?}',
  phases: [
    { title: 'Qualify', detail: 'one agent per chunk of leads: score + reply draft' },
    { title: 'Merge', detail: 'dedupe near-identical posters, rank, write .ranked.json' },
  ],
}

// args: { nightFile: 'leads/nightly/YYYY-MM-DD.json', pids: ['123','456',...], chunk: 8 }
const nightFile = args && args.nightFile
const pids = (args && args.pids) || []
const CHUNK = (args && args.chunk) || 8
if (!nightFile) throw new Error('args.nightFile required')
if (!pids.length) { log('0 leads to qualify, nothing to do'); return { ranked: [], rankedFile: null } }

const LEAD = {
  type: 'object',
  properties: {
    pid: { type: 'string' }, section: { type: 'string' },
    score: { type: 'number' }, tier: { type: 'string', enum: ['A', 'B', 'C'] },
    budget: { type: 'string' }, timeline: { type: 'string' }, area: { type: 'string' }, beds: { type: 'string' },
    why: { type: 'string' }, red_flags: { type: 'array', items: { type: 'string' } },
    contact: { type: 'object', properties: {
      reply_email: { type: 'string' }, emails_in_post: { type: 'array', items: { type: 'string' } },
      phones_in_post: { type: 'array', items: { type: 'string' } } } },
    reply_draft: { type: 'string' },
  },
  required: ['pid', 'score', 'tier', 'why', 'reply_draft'],
}
const QUALIFY = { type: 'object', properties: { leads: { type: 'array', items: LEAD } }, required: ['leads'] }

const chunks = []
for (let i = 0; i < pids.length; i += CHUNK) chunks.push(pids.slice(i, i + CHUNK))
log(`${pids.length} leads in ${chunks.length} chunk(s)`)

phase('Qualify')
const results = await parallel(chunks.map((ids, i) => () => agent(
`Read leads/qualify_rules.md and leads/reply_rules.md, then Read ${nightFile}.
Handle ONLY the leads whose pid is in: ${JSON.stringify(ids)}.
For each: score with the rubric, assign tier, extract budget/timeline/area/beds ("unknown" if absent), write why (1 line), red_flags, copy contact fields from the lead (reply_email, emails_in_post, phones_in_post), and write reply_draft per reply_rules.md.
Rotate the free-service line across your leads (chunk ${i + 1}, start with option ${(i % 3) + 1}).
Hard checks before returning: no em dash character anywhere in reply_draft, at most 3 emoji, signature exactly "Sophia Reddehase | Spirit Real Estate Group | TREC #831516".
A lead with "error": "removed" gets score 0, tier C, why "post removed".`,
  { label: `qualify:${i + 1}/${chunks.length}`, phase: 'Qualify', schema: QUALIFY }
)))
const qualified = results.filter(Boolean).flatMap(r => r.leads)
log(`${qualified.length}/${pids.length} qualified (A: ${qualified.filter(l => l.tier === 'A').length}, B: ${qualified.filter(l => l.tier === 'B').length})`)
if (qualified.length < pids.length) log(`WARNING: ${pids.length - qualified.length} lead(s) dropped by failed agents`)

phase('Merge')
const rankedFile = nightFile.replace(/\.json$/, '.ranked.json')
const merge = await agent(
`Here are tonight's qualified leads as JSON:
${JSON.stringify(qualified)}

1. Read ${rankedFile} if it exists; it holds leads ranked earlier tonight. Union them with the new ones (new data wins on the same pid).
2. Dedupe near-identical posters (same phone/email, or same title+body reposted in another section): keep the highest score, list the other pids in "dupes".
3. Sort by score desc. Keep tiers A and B in "ranked"; put C in "dropped" (pid, score, why only).
4. Write the full object {night: "<date from filename>", ranked: [...], dropped: [...], counts: {A, B, C}} to ${rankedFile} with the Write tool.
Return counts and the top 5 pids.`,
  { label: 'merge+rank', phase: 'Merge',
    schema: { type: 'object', properties: {
      counts: { type: 'object', properties: { A: { type: 'number' }, B: { type: 'number' }, C: { type: 'number' } } },
      top: { type: 'array', items: { type: 'string' } } }, required: ['counts', 'top'] } }
)
return { rankedFile, counts: merge && merge.counts, top: merge && merge.top }
