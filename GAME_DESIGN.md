# Pokémon Crown & Chaos — High-Level Game Design

## 1. Core vision

**Crown & Chaos** is a long-form GBA monster-battling adventure about John, a
young traveler asked to decide what worthy leadership looks like when inherited
institutions fail. John begins with the **Water-type starter**. Candy, a major
companion and rival with her own goals, begins with the **Fire-type starter**.

The player explores the original **Aurelia Region**, builds a party of original
creatures, earns eight major progression seals, confronts a movement exploiting
an ancient succession crisis, and discovers optional stories that change the
meaning—not the basic availability—of the finale. The tone balances warmth,
mystery, humor, moral seriousness, and hope. Target rating and exact terminology
will be confirmed before the vertical slice.

### Design pillars

1. **A journey with consequences:** characters remember aid, neglect, and mercy;
   side stories develop communities without trapping players in opaque morality.
2. **Exploration rewards attention:** visual clues, shortcuts, layered traversal,
   optional interiors, rumors, and revisitable spaces replace constant signposting.
3. **Readable tactical battles:** clear rules and strong creature identities create
   decisions through party synergy, status, terrain, and resource timing.
4. **Companions with agency:** Candy and other rivals act offscreen, disagree
   honestly, and grow without existing only to praise or obstruct John.
5. **Earned abundance:** 40+ hours comes from varied authored content and mastery,
   not mandatory grind, maze padding, or repeated dialogue.
6. **Handheld polish:** fast startup, responsive menus, legible UI, reliable saves,
   concise scenes, stable frame pacing, and excellent moment-to-moment feedback.

## 2. Setting and thematic framework

Aurelia encircles a highland basin whose waterways and roads once joined several
self-governing provinces. Its ceremonial crown is not a magic entitlement to
rule; it represents a covenant of service. The crown disappeared during an old
schism, and regional institutions now compete over who may restore it.

The antagonist faction, provisionally **the Concord of Glass**, promises perfect
order by awakening a force that can suppress uncertainty and choice. Its members
range from frightened citizens to ambitious leaders; the story should distinguish
misguided people from harmful choices. A chaotic counterforce tempts others to
reject all obligation. John and Candy discover that neither domination nor
aimlessness can sustain a community.

Catholic-inspired themes may appear through fictional symbols and story patterns:
pilgrimage, conscience, confession and repair, freely chosen sacrifice, mercy,
stewardship, hospitality, dignity, death and hope, and authority as service.
Architecture may use cloisters, bells, gardens, mosaics, and processional paths
without copying particular sacred objects as collectible power-ups. The game must
not claim its fictional cosmology is Catholic doctrine, caricature clergy or
worship, make sacraments into mechanics, or require the player to share a faith.
Relevant material receives informed sensitivity review.

## 3. Player experience and progression

### Main loop

Explore → observe clues and meet people → battle/recruit creatures → solve local
problems → earn access or traversal capability → revisit earlier spaces → refine
the party → advance character and regional stories.

### Adventure shape

- **Prologue (1–2 hours):** John's home near the headwaters; starter choice is
  fixed to Water for the canonical campaign, Candy receives Fire; tutorial journey
  and a disruptive event establish their friendship and disagreement.
- **Act I (6–8 hours, seals 1–2):** two provinces reveal failing infrastructure,
  local stakes, a rival, and the Concord's appealing public face.
- **Act II (10–12 hours, seals 3–5):** travel opens; competing factions and Candy's
  independent investigation complicate the crown legend; layered backtracking and
  larger optional areas begin.
- **Act III (10–12 hours, seals 6–8):** consequences converge, antagonists fracture,
  and difficult dungeons test team-building and navigation.
- **Finale (4–6 hours):** pilgrimage toward the Crown Seat, faction resolution,
  championship/major-battle sequence, final decision, aftermath, and credits.
- **Post-game (6–10+ hours):** new chapter, remote zone, rematches, challenge
  facility, superbosses, collection goals, and character/settlement epilogues.

Main credits should take roughly **32–38 hours** for an engaged first-time player;
substantial optional and post-game material brings the intended experience above
**40 hours**. Playtests, not word or map counts, determine the final duration.

### Progression model

Eight **Covenant Seals** (working name) structure regional progression. Each is
earned through a leader-focused trial combining a themed place, civic problem,
and climactic battle—not eight interchangeable rooms. Seals unlock the finale and
signal recommended challenge order. Traversal techniques unlock shortcuts and
optional branches but should not force a party member to carry weak utility moves.

The route is guided-open: early and late anchors are fixed, while selected middle
provinces can be tackled in pairs. Level/difficulty bands and story-state variants
support flexibility without universal enemy scaling. The journal distinguishes
main objectives, leads, optional quests, and discoveries.

## 4. World-design principles

- **Regional logic:** geology, climate, roads, watersheds, economies, settlement
  placement, and creature habitats must make sense together.
- **Landmark navigation:** every major screen has a recognizable silhouette,
  palette purpose, or spatial clue; maps avoid featureless corridors.
- **Loops and layers:** routes contain visible future paths, unlockable shortcuts,
  elevation/water layers, and at least one meaningful optional discovery.
- **Dense towns:** distinctive services, recurring residents, interiors, evolving
  dialogue, and local quests matter more than empty building count.
- **Dungeon identity:** each major dungeon combines a traversal grammar, ecology,
  narrative purpose, escalating variations, a respite, and a memorable payoff.
- **Fair secrets:** environmental language and rumors hint at discoveries; rewards
  are valuable without making blind wall-checking mandatory.
- **State discipline:** permanent changes are planned as explicit variants so NPCs,
  collision, warps, and quests cannot drift into contradictory states.

### Proposed content envelope

Targets are planning ranges, subject to cartridge and production budgets:

| Content | Approximate target |
| --- | ---: |
| Major settlements | 10–12 |
| Routes/open traversal areas | 24–30 |
| Major dungeons/landmarks | 12–16 |
| Small optional caves/interiors | 20–30 |
| Major progression trials | 8 |
| Rival/set-piece battles | 12–18 |
| Main-story quests/chapters | 35–45 |
| Authored side quests/chains | 40–60 |
| Original recruitable creature species | 120–160 |
| Major NPC trainers | 180–240 |
| Post-game zones/facilities | 3–5 |

Counts are not success criteria. Each entry must have a gameplay or narrative
purpose, and scope can be reduced to preserve quality.

## 5. Major gameplay systems

### Creatures, party, and growth

- A roster of original species organized by habitat, role, growth curve, and
  evolutionary family; silhouettes and palette usage must remain GBA-readable.
- Party of up to six, persistent storage, bestiary research, experience/levels,
  evolutions, learnsets, conditions, equipment/held-item analogue, and naming.
- Starter trio has equally complete arcs. John's Water starter emphasizes adaptive
  defense/tempo; Candy's Fire starter emphasizes initiative/risk. Exact species
  designs wait for roster and legal/style review.
- Avoid required grinding through encounter pacing, experience tuning, optional
  trainer density, catch-up support, and predictable boss preparation.

### Battles

Turn-based party battles with a compact elemental chart, physical/special/status
roles, accuracy, priority, switching, persistent conditions, limited field effects,
trainer AI archetypes, and boss phase/strategy design that obeys player-facing
rules. Most battles are fast single encounters; doubles or special formats appear
selectively after dedicated onboarding.

Fairness rules: important threats are telegraphed, unavoidable randomness is
bounded, bosses do not secretly invalidate systems, and defeat returns the player
quickly with understandable cost. A deterministic simulation harness should test
damage, effects, AI legality, and balance distributions.

### Exploration and interaction

Four-direction movement, running, contextual interaction, collision/elevation,
warps, moving NPCs, inspectable environments, item finds, field encounters,
weather/lighting used sparingly, traversal techniques, shortcuts, and a map/journal.
Puzzles test observation and system understanding rather than obscure inputs.

### Quests and choices

Quest states use explicit prerequisites, objectives, outcomes, and recovery paths.
Side quests mix investigation, exploration, battles, delivery with decisions,
habitat research, community repair, and recurring character chains. Choices change
dialogue, relationships, local visuals, or rewards when production allows, while
the main ending remains testable and coherent. No important quest should silently
expire without warning.

### Economy and rewards

Currency supports healing supplies, capture tools, travel conveniences, and
optional customization. Exploration yields unique techniques, creature access,
lore, shortcuts, and character scenes—not only consumables. Sinks scale without
punishing experimentation; sell prices and repeatable rewards resist exploits.

### Dialogue and presentation

Portrait-free or limited-portrait scenes should use expressive sprites, blocking,
camera, sound, and concise text. Dialogue tooling must validate line width, box
count, speaker, control tokens, and localization headroom. Skippable repeat scenes,
fast text, battle animation options, clear icons plus text, and readable contrast
are baseline goals.

### Saving and technical UX

Save anywhere safe or at clearly defined points after feasibility testing. Use
checksums, versioning, staged/atomic writes, recovery behavior, and explicit errors.
Track play time, options, party/storage, inventory, world flags, quest state,
collectibles, and post-game state. Never risk an existing save merely to add a
feature; migration tests are required.

## 6. Principal characters and arcs

- **John:** player character. Characterization comes from dependable actions and
  bounded dialogue choices; he grows from proving capability to understanding
  service and shared responsibility.
- **Candy:** co-lead and friendly rival, not a passive guide. Brave, impatient with
  hollow ceremony, and protective of overlooked communities. Her Fire starter and
  independent investigations produce a parallel progression visible in battles.
  She can challenge John without becoming a villain or prize.
- **Regional leaders:** eight distinct custodians whose civic strengths and blind
  spots embody aspects of authority. Their post-trial lives continue through
  rematches, quests, and crisis participation.
- **Rivals:** at least one mechanics-focused peer and one ideology-focused foil
  create recurring contrasts without duplicating Candy's role.
- **Concord ensemble:** named members occupy different moral positions and respond
  differently when the faction's real plan is revealed.

Names beyond John and Candy are provisional until narrative and cultural review.

## 7. Optional and post-game content

Optional content should form a web rather than a late checklist: hidden habitats,
multi-stage NPC stories, ecological puzzles, rare creature families, route mastery,
leader rematches, folklore investigations, and revisited towns that visibly change.
At least one optional through-line begins in each act and resolves after the finale.

The post-game opens because of the ending rather than pretending it did not occur.
Its pillars are: a 2–3 hour narrative chapter, a mechanically distinctive remote
zone, scalable rematches, a replayable challenge facility, several authored
superbosses, difficult secrets, roster completion tools, and epilogues for major
quest chains. It must receive the same save, balance, and copy-editing QA as the
main campaign.

## 8. Definition of “polished”

- No progression blockers, data-loss bugs, placeholder assets, broken links, or
  known critical defects.
- Consistent UI language, animation timing, sound feedback, naming, and writing.
- Stable frame pacing and measured memory/ROM headroom in stress cases.
- Fast common actions and low-friction recovery from battle loss or mistakes.
- Main, optional, and post-game content is discoverable, rewarding, and tested.
- Credits and license records cover every dependency and asset.
- Complete start-to-post-game validation on 44VBA, emulator cross-checks, and
  hardware testing where available.
