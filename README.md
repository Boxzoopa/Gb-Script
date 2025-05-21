# GBScript
A Programming Language for the Gameboy

**GBScript** is a custom scripting language designed for retro game development, inspired by Lua and C. It targets the Game Boy via transpilation to C (e.g., GBDK-compatible output). GBScript aims to provide a modern, readable syntax for defining game logic while staying within the technical limits of retro hardware.

## ✨ Goals

* Fast and flexible scripting for retro consoles
* Simple syntax: no mandatory semicolons, Python/Lua-style control flow
* Built-in support for sprites, music, and game logic primitives
* Modular structure with cross-file includes
* Compiles to optimized C for use with GBDK and similar retro dev kits

---

## ✅ Current Features

* Basic variable declarations (`var`, `const`)
* Type annotations (`: int`, `: str`) with type-checking
* Expression parsing with proper precedence (`+`, `-`, `*`, `/`)
* Grouped expressions `( ... )`
* Unary minus (`-x`)
* String and number literals
* Semicolon optional (currently required for statements)

---

## 🔧 Planned Features / TODO

### Language Features

* [ ] `if` / `elif` / `else` statements
* [ ] `while` and `for` loops
* [ ] Function declarations and calls
* [ ] Arrays and indexing (`arr[0]`)
* [ ] Struct-like custom types or record tables
* [ ] Import / include (`load_file("player.gbs")`)
* [ ] Native constants and macros

### Runtime / Game Features

* [ ] `load_sprite()`, `draw_sprite()` support for GBDK
* [ ] Background/map support (tilemaps)
* [ ] Music/sound scripting (note-by-note tracker syntax)
* [ ] Game loop abstraction (`main.gbs` vs helper modules)

### Transpiler Enhancements

* [ ] Semantic analyzer (catch undeclared vars, type mismatches)
* [ ] Dead code elimination
* [ ] Optimized transpilation to C (or ASM targets later)
* [ ] Debug mode with symbol mapping and print support

---

## 📦 Example

```gbs
var x: int = 5;
const message: str = "Hello!";

if x > 3 {
  draw_text(message, 10, 10);
}
```

---

## 🧪 Getting Started

Coming soon: CLI tool and documentation for compiling `.gbs` files to `.c`.

---

Let me know if you want this split into multiple files like `CONTRIBUTING.md`, `TODO.md`, etc.
