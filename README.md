# FS25 Extract source code

## 1. Preparation

- Install python
- Install rust
- Create a new folder on your system
- Download [QuickBMS](https://aluigi.altervista.org/quickbms.htm) in a subfolder named "quickbms"
- Download [Medal Lua decompiler](https://github.com/scfmod/medal) in a subfolder named "medal"


## 2. Extract game archive

Run this command to create a new folder named "l64" containing raw games sources. Press y when prompted to load dll
```
quickbms\quickbms.exe extract_fs25_sourcecode\gar_giants.txt "C:\Program Files (x86)\Steam\steamapps\common\Farming Simulator 25\dataS.gar" l64
```

## 3. Decode scripts l64 files

Run this command to decode the .l64 files in place (files' content is replaced with decoded content)
```
python extract_fs25_sourcecode\l64Decoder.py l64
```

## 4. Decompile lua scripts

Make sure you have the nightly version installed
```
rustup install nightly
```

Decompte lua scripts
```
python extract_fs25_sourcecode\decompile_lua.py medal l64 <output_path>
```

## 5. Enjoy
That's it! You should now have a folder containing all FS25 lua scripts.

Note: The names of the local variables and functions arguments are obfuscated, but the names of the functions and global variables are not.



# Credits
- @TAEMBO for the QuickBMS script `gar_giants.txt`
- @Rockstar94FS for the l64 file decoder `l64Decoder.py`
