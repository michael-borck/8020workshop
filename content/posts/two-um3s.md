---
title: "Two Ultimaker 3s, 30 Rolls of Filament, $150 AUD"
date: 2026-02-23
tags: ["printing", "ultimaker", "80-20", "restoration", "marketplace"]
---

## How a Facebook Marketplace Impulse Buy Turned Into the Perfect Specialist Machine

*80-20 Workshop*

---

There's a moment in every marketplace scroll where your brain does the math before your fingers can type "is this still available?" Two Ultimaker 3 printers. One standard, one Extended. Thirty rolls of filament. $150 AUD for the lot.

The seller was an engineering company clearing house after switching to Bambu Lab. He mentioned one had a "locked up" extruder, called the machines "finicky," and said the filament was "waterlogged." He also didn't seem to care whether I showed up or not.

I showed up.

### What $150 Actually Gets You

Let's do the honest maths. Even at fire-sale prices, 30 rolls of 2.85mm filament (mostly Nylon, ASA, PLA, and PVA) would run $500-600 AUD if you bought them fresh. A single genuine Ultimaker Print Core costs $200+. The machines themselves, when new, sold for over $3,000 each. Even accounting for age and condition, this is the kind of deal that makes the 80-20 philosophy feel almost unfair.

But deals like this come with uncertainty. Would the electronics boot? Were the custom mainboards fried alongside the supposedly waterlogged filament? Could I actually get prints out of a machine designed for corporate engineers and then abandoned for a Bambu?

### First Impressions at the Bench

Both machines are dusty but structurally solid. The Ultimaker 3 uses a composite panel frame, not thin aluminium extrusions, so there's no rack or twist even after years of storage and a car ride home. The semi-enclosed design (open front, enclosed sides and back) was ahead of its time. These things shipped with a built-in camera, NFC filament detection, network printing, and mechanical dual extrusion. In 2016, this was a spaceship.

The motion system is fascinating if you come from the Prusa/Ender world. It's a "crossed gantry" Cartesian system where the heavy stepper motors sit fixed to the frame and drive rotating rods around the perimeter. Short belts spin those rods, which pull longer belts connected to sliding blocks. The result is an extremely lightweight print head that changes direction smoothly with minimal ghosting. The bed only moves on the Z-axis, slowly dropping a fraction of a millimetre per layer. No bedslinging, no wobble on tall prints.

The inner cross-rods that guide the hotend have some surface rust. They'll need a polish with 0000 steel wool and a drop of sewing machine oil. Not sandpaper, because those rods are precision-ground. You polish them, you don't grind them.

### The Power-On Moment

Both machines boot. Both heat beds and hotends. Both home X, Y, and Z. The mechanical nozzle lift (where the inactive nozzle physically clicks up on a spring-loaded hinge) works perfectly on both. This is a genuinely impressive mechanism: a lever on the gantry frame pushes the second nozzle down when it needs to print, and a spring pulls it back when it's done, keeping it from dragging across your part. No servo, no electronics. Pure mechanical design.

### Reading the Black Box

The Print Core stats tell the real story. Each core has a tiny EEPROM chip that tracks its own usage, independent of the printer. Factory reset won't erase them. You could pull a core from one machine, plug it into another, and the stats follow.

**UM3 Extended:**
- PC1 (AA 0.4): 108 days print time, 1,666m of material extruded, max temp 284C
- PC2 (BB 0.4): 59 days, 229m, max temp 272C (visible PVA blob on the nozzle)

**UM3 Standard:**
- PC1 (AA 0.4): 10 hours, 3.82m, max temp 246C
- PC2 (BB 0.4): 53 days, 162m, max temp 354C (that 354C reading is suspicious, likely a thermistor glitch)

The standard UM3's AA core has barely been touched. Someone bought a $200+ replacement Print Core, ran half a dozen test prints, then the Bambu arrived and everything went into storage. That's a near-new core sitting in my workshop for free.

The 108-day core on the Extended is a workhorse that's been through a full life of engineering prints. It's near end of life but will keep going on non-abrasive materials (PLA, PETG, standard Nylon). Just avoid glow-in-the-dark, carbon fibre, wood-fill, or metal-fill, all of which grind brass nozzles to nothing.

### The "Waterlogged" Filament Myth

"Waterlogged" in 3D printing almost never means the filament was sitting in water. It means it absorbed moisture from ambient humidity over time. Engineering filaments like Nylon and PVA are aggressively hygroscopic. Wet PVA in a heated nozzle turns into a boiling, popping, clogging disaster, which is almost certainly what killed the "locked up" extruder.

The fix is straightforward: run the filament through a food dehydrator at the appropriate temperature for 8-24 hours depending on material. And then store it properly in sealed bags with desiccant, especially the PVA.

Here's the beautiful irony though: the "waterlogged" Nylon is actually perfect for cold pulls (atomic pulls). Wet Nylon steams inside the heated nozzle, acting like a miniature pressure washer to loosen baked-on residue. And unlike wet PLA, which goes brittle and snaps inside the heat break, wet Nylon stays incredibly flexible and tough. You can yank it out without fear of it breaking off and making the problem worse.

### The Specialist Role

I already have a Prusa MK3S+ that handles 90% of everyday printing beautifully. Direct drive, 1.75mm filament, crisp retractions, handles flexibles, massive community support. The Ultimaker doesn't replace any of that.

What the Ultimaker does is fill a very specific gap: complex geometry with soluble supports. Load PLA (or ASA, or Nylon) in nozzle one, PVA in nozzle two, and print parts with internal cavities, crazy overhangs, and print-in-place mechanisms. Drop the finished part in warm water overnight, the PVA dissolves, and you're left with something that would be physically impossible to clean up with standard break-away supports.

The 300mm Z-height on the Extended version is the cherry on top. Because the bed doesn't sling back and forth, tall parts stay perfectly still. No wobble, no layer shifting at the top. You can print a 300mm tall cylinder and the top layers will look as clean as the bottom.

First real project: a custom snorkel for my 2008 Kia Sorento, printed in ASA (UV-resistant, heat-resistant, impact-tough), split into interlocking sections to fit the build volume, chemically welded and sealed with Sikaflex.

### The 80-20 Take

The Ultimaker 3 Extended is not a modern speed demon. It doesn't have input shaping or linear advance. The 2.85mm filament ecosystem is shrinking at the hobbyist retail level (though enterprise and education suppliers will stock it indefinitely because Ultimaker dominates those markets). The Print Cores are expensive consumables if you need to replace them.

But I didn't pay modern speed demon prices. I paid $150 for two machines, a near-new spare Print Core, a donor machine worth hundreds in parts, and enough filament to last a year. The firmware is mature and stable (final version 5.3.0). Cura profiles are bulletproof for the dual-extrusion workflow. The mechanical design is over-engineered and built to last.

Sometimes the 80-20 move isn't about buying the best new thing. It's about recognising when someone else's "obsolete" is your perfect specialist tool.

---

*The restoration continues this weekend. Rods to polish, PVA blobs to dissolve, firmware to update from 4.3.3 to 5.3.0 (via the mandatory 4.3.97 stepping-stone, because Ultimaker changed file formats mid-lifecycle). Follow along for the full teardown and first dual-extrusion print.*
