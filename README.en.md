# HD2D Skill

**Pixel art in 3D spaces · 像素三维场景搭建**

[中文](README.md) | English

A reusable agent skill for building HD2D scenes: simple 3D geometry provides volume, perspective and occlusion; pixel art, camera work and lighting shape the visual style. Use it for games, interactive illustrations, virtual spaces or visual presentations, across themes, engines and platforms.

Includes two standalone HTML demos: **Rain Harbor — Neon Night Walk** and **A Thousand Li of Rivers and Mountains**. This README is available in English; the skill instructions, detailed references and demo interfaces are currently in Chinese. You can ask your agent to explain and apply the guidance in English.

## Animated previews

### Rain Harbor — Neon Night Walk

![Rain Harbor animation: a pixel character runs through neon streets with splashes and wet-ground reflections](assets/previews/rain-harbor.gif)

Modular buildings, perspective camera movement, pixel characters, neon glow and water interaction. [Download and open the Rain Harbor demo](assets/demos/雨港.html).

### A Thousand Li of Rivers and Mountains

![Landscape animation: a character travels past a stone bridge, water and layered blue-green mountains](assets/previews/mountains-and-rivers.gif)

A blue-green landscape with bridges, pavilions, vegetation, water and depth parallax. [Download and open the landscape demo](assets/demos/千里江山.html).

These silent GIFs come from scene recordings with the controls hidden. Each loops a 4-second clip at 640 × 360. Frame rate and color count are reduced for page loading; open the HTML demos for the full lighting, audio and interaction.

## Quick start

1. Download and extract this repository or the shareable ZIP. Rename the extracted folder to `hd2d-scene-builder`. The repository is named `hd2d-skill`; the skill identifier remains `hd2d-scene-builder`.
2. Put the entire folder in the skills directory of an agent tool that supports `SKILL.md`. For Codex, use `$CODEX_HOME/skills/`, or `~/.codex/skills/` when `CODEX_HOME` is not set.
3. Start a new session and invoke `$hd2d-scene-builder`. Specify your theme, camera, target platform and desired interactions. Other tools may use different installation and invocation conventions.

Example prompts:

> Use $hd2d-scene-builder to create a portrait-format woodland village with a perspective camera and a character walking along a stone path. Validate a small layout and an asset sample before expanding the scene. Explain your work in English.

> Use $hd2d-scene-builder to investigate flickering highlights in this existing pixel-art 3D scene. Preserve the pixel-art brushwork, identify the source of instability, then adjust lighting and sampling as needed.

You can also read [SKILL.md](SKILL.md) directly. This is a workflow for an agent to implement, rather than a standalone scene-generation application. Characters, movement, water, weather and audio are optional.

## Run the demos

After downloading, open either HTML file in a browser with **WebGL 2 and hardware acceleration** enabled. JavaScript, styles, images and audio resources are embedded; no CDN or asset service is required. Click the on-screen sound button to enable audio. GitHub's file view displays source code, so download the file before opening it in your browser.

| Demo | Highlights | Main controls |
| --- | --- | --- |
| [Rain Harbor](assets/demos/雨港.html) | Perspective streets, neon lighting, reflections, walking and running splashes | WASD / arrow keys to walk; Shift to run; click the ground to move; right-drag to look around; wheel to zoom; E to interact |
| [Rivers and Mountains](assets/demos/千里江山.html) | Blue-green mountains, water, dawn/dusk changes and environmental interactions | A / D or left/right arrows to walk; Shift to run; Space to jump; E to interact; click the path or a route destination to move |

Both demos include on-screen controls; Esc pauses or closes a dialog. Landscape orientation is recommended for Rivers and Mountains. See the [demo notes](assets/demos/README.md) for further details in Chinese.

The demos are self-contained finished snapshots, with their code embedded in HTML. The original editable asset projects and complete development/build pipelines are not included. Use the skill and references to build new scenes with your own tools and assets.

## What's inside

| Resource | Covers |
| --- | --- |
| [SKILL.md](SKILL.md) | Scope, blockout, modular construction, cameras, interaction and delivery |
| [Pixel art](references/pixel-art.md) | Drawing workflow, pixel density, tiling, character animation, pivots, atlases and sampling |
| [Lighting and stability](references/lighting-stability.md) | Lighting layers, motion flicker diagnosis, bloom and anti-aliasing trade-offs |
| [Water and interaction](references/water.md) | Reflection choices, ripple limits, water-contact events and performance budgets |

## Validate and package

Requires Python 3.10 or later; only the standard library is used. Run from the repository root:

```text
python tools/release.py check
python tools/release.py pack
```

Checks cover required files, local links, basic GIF format and size, external HTML dependencies, known machine-path and credential patterns, and license notices. Packaging validates first, then creates `dist/hd2d-scene-builder.zip` with an enclosing `hd2d-scene-builder` folder. Both READMEs, demos and preview GIFs are included; Git history, caches, personal settings and previous ZIPs are excluded.

Static checks do not replace browser rendering or target-device tests. Performance, mobile layout and audio behavior need to be verified in your intended environment. Water patterns and particles are visual approximations, not a full fluid simulation.

## License

Original documentation, code and original demo content are released under the [MIT License](LICENSE). Third-party components retain their own licenses; see [Third-party notices](THIRD_PARTY_NOTICES.md).
