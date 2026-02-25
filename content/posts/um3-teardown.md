---
title: "Ultimaker 3 Teardown: What I Found Inside"
date: 2026-02-24
tags: ["printing", "ultimaker", "restoration"]
---

With both Ultimaker 3s on the bench, it's time to dig into what makes these machines tick — and what needs fixing.

### The Motion System

The UM3 uses a "crossed gantry" Cartesian system that's fascinating if you come from the Prusa/Ender world. The heavy stepper motors sit fixed to the frame and drive rotating rods around the perimeter. Short belts spin those rods, which pull longer belts connected to sliding blocks. The result is an extremely lightweight print head that changes direction smoothly with minimal ghosting. The bed only moves on the Z-axis, slowly dropping a fraction of a millimetre per layer. No bedslinging, no wobble on tall prints.

The inner cross-rods that guide the hotend have some surface rust. They'll need a polish with 0000 steel wool and a drop of sewing machine oil. Not sandpaper — those rods are precision-ground. You polish them, you don't grind them.

### Reading the Black Box

Each Print Core has a tiny EEPROM chip that tracks its own usage, independent of the printer. Factory reset won't erase them. Pull a core from one machine, plug it into another, and the stats follow.

**UM3 Extended:**
- PC1 (AA 0.4): 108 days print time, 1,666m of material, max temp 284C
- PC2 (BB 0.4): 59 days, 229m, max temp 272C (visible PVA blob on the nozzle)

**UM3 Standard:**
- PC1 (AA 0.4): 10 hours, 3.82m, max temp 246C
- PC2 (BB 0.4): 53 days, 162m, max temp 354C (suspicious — likely a thermistor glitch)

The standard UM3's AA core has barely been touched. Someone bought a replacement Print Core, ran half a dozen test prints, then the Bambu arrived and everything went into storage. That's a near-new core sitting in my workshop.

The 108-day core on the Extended is a workhorse near end of life, but it'll keep going on non-abrasive materials. Just avoid glow-in-the-dark, carbon fibre, wood-fill, or metal-fill — all of which grind brass nozzles to nothing.

### The "Waterlogged" Filament

"Waterlogged" in 3D printing almost never means the filament was sitting in water. It means it absorbed moisture from ambient humidity over time. Engineering filaments like Nylon and PVA are aggressively hygroscopic. Wet PVA in a heated nozzle turns into a boiling, popping, clogging disaster — which is almost certainly what killed the "locked up" extruder.

The fix: run the filament through a food dehydrator at the appropriate temperature for 8-24 hours depending on material. Then store it properly in sealed bags with desiccant.

Here's the beautiful irony though: the "waterlogged" Nylon is actually perfect for cold pulls. Wet Nylon steams inside the heated nozzle, acting like a miniature pressure washer to loosen baked-on residue. And unlike wet PLA, which goes brittle and snaps inside the heat break, wet Nylon stays incredibly flexible and tough. You can yank it out without fear of it breaking off and making the problem worse.

### What's Next

Firmware needs updating from 4.3.3 to 5.3.0, via the mandatory 4.3.97 stepping-stone (Ultimaker changed file formats mid-lifecycle). After that: first dual-extrusion test print, and then the real project — a custom snorkel for my 2008 Kia Sorento, printed in ASA, split into interlocking sections, chemically welded and sealed with Sikaflex.
