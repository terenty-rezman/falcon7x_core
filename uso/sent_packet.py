import math

import numpy as np

# FROM_MODEL PACKET

uso_float_field_names = [

]

uso_bitfield_names = [
# ---------------- Сигналы в УСО ----------------------
	"O10_a12",	# PTY стрелка OUT [K2 Средний пульт (Pedestal)] [Козырек приборной доски] [22 Пульт козырька левый]
	"O10_a13",	# PTY надпись OUT [K2 Средний пульт (Pedestal)] [Козырек приборной доски] [22 Пульт козырька левый]
	"O10_a14",	# MASTER WARNING light OUT [K2 Средний пульт (Pedestal)] [Козырек приборной доски] [22 Пульт козырька левый]
	"O10_a15",	# MASTER CAUTION light OUT [K2 Средний пульт (Pedestal)] [Козырек приборной доски] [22 Пульт козырька левый]
	"O10_a16",	# PTY стрелка OUT [K2 Средний пульт (Pedestal)] [Козырек приборной доски] [23 Пульт козырька правый]
	"O10_a17",	# PTY надпись OUT [K2 Средний пульт (Pedestal)] [Козырек приборной доски] [23 Пульт козырька правый]
	"O10_a18",	# MASTER WARNING light OUT [K2 Средний пульт (Pedestal)] [Козырек приборной доски] [23 Пульт козырька правый]
	"O10_a19",	# MASTER CAUTION light OUT [K2 Средний пульт (Pedestal)] [Козырек приборной доски] [23 Пульт козырька правый]
	"O10_a04",	# 115/230 индикатор [K2 Средний пульт (Pedestal)] [Приборная доска] [03 - 15 Рукоятка аварийного/стояночного тормоза (#--#) - Кнопка-переключатель 115/220]
	"O26_a32",	# DIM [K2 Средний пульт (Pedestal)] [Приборная доска] [03 - 15 Рукоятка аварийного/стояночного тормоза (#--#) - Кнопка-переключатель 115/220]
	"O26_a30",	# TEST [K2 Средний пульт (Pedestal)] [Приборная доска] [03 - 15 Рукоятка аварийного/стояночного тормоза (#--#) - Кнопка-переключатель 115/220]
	"O10_a01",	# РУД 3 лампы <red light> [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [01 Сборка РУД]
	"O10_a02",	# РУД 3 лампы <red light> [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [01 Сборка РУД]
	"O10_a03",	# РУД 3 лампы <red light> [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [01 Сборка РУД]
	"O10_a05",	# AURAL WARN 1 OUT <OFF> [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [12  (Emergency Panel)]
	"O10_a06",	# AURAL WARN 1 OUT <OFF> [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [12  (Emergency Panel)]
	"O10_a07",	# BAG FAN OUT <ON> [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [12  (Emergency Panel)]
	"O10_a08",	# ELEC RH ESS OUT <ISOL> [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [12  (Emergency Panel)]
	"O10_a09",	# FUEL 2 B/U OUT <INHIBIT> [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [12  (Emergency Panel)]
	"O10_a10",	# RAT AUTO OUT <ON> [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [12  (Emergency Panel)]
	"O10_a11",	# TRIM EMERG OUT <ON> [K2 Средний пульт (Pedestal)] [Средний пульт (Pedestal)] [12  (Emergency Panel)]
	"O10_a20",	# engine 1 shut off FIRE <CLOSED> [K4 Верхний пульт] [Верхний пульт] [01 (Fire Control Panel) Пульт пожарной сигнализации]
	"O10_a21",	# engine 1 DISCH 1 <1> [K4 Верхний пульт] [Верхний пульт] [01 (Fire Control Panel) Пульт пожарной сигнализации]
	"O10_a22",	# engine 1 DISCH 1 <DISCH> [K4 Верхний пульт] [Верхний пульт] [01 (Fire Control Panel) Пульт пожарной сигнализации]
	"O10_a23",	# engine 1 DISCH 2 <1> [K4 Верхний пульт] [Верхний пульт] [01 (Fire Control Panel) Пульт пожарной сигнализации]
	"O10_a24",	# engine 1 DISCH 2 <DISCH> [K4 Верхний пульт] [Верхний пульт] [01 (Fire Control Panel) Пульт пожарной сигнализации]
	"O10_a25",	# FIRE APU <DISCH> [K4 Верхний пульт] [Верхний пульт] [01 (Fire Control Panel) Пульт пожарной сигнализации]
	"O10_a26",	# FIRE APU <CLOSED> [K4 Верхний пульт] [Верхний пульт] [01 (Fire Control Panel) Пульт пожарной сигнализации]
	"O10_a27",	# engine 2 shut off FIRE 2 <CLOSED> [K4 Верхний пульт] [Верхний пульт] [01 (Fire Control Panel) Пульт пожарной сигнализации]
	"O10_a28",	# engine 2 DISCH 1 <1> [K4 Верхний пульт] [Верхний пульт] [01 (Fire Control Panel) Пульт пожарной сигнализации]
	"O10_a29",	# engine 2 DISCH 1 <DISCH> [K4 Верхний пульт] [Верхний пульт] [01 (Fire Control Panel) Пульт пожарной сигнализации]
	"O10_a30",	# engine 2 DISCH 2 <1> [K4 Верхний пульт] [Верхний пульт] [01 (Fire Control Panel) Пульт пожарной сигнализации]
	"O10_a31",	# engine 2 DISCH 2 <DISCH> [K4 Верхний пульт] [Верхний пульт] [01 (Fire Control Panel) Пульт пожарной сигнализации]
	"O10_a32",	# engine 3 shut off FIRE 3 <CLOSED> [K4 Верхний пульт] [Верхний пульт] [01 (Fire Control Panel) Пульт пожарной сигнализации]
	"O10_b01",	# engine 3 DISCH 1 <1> [K4 Верхний пульт] [Верхний пульт] [01 (Fire Control Panel) Пульт пожарной сигнализации]
	"O10_b02",	# engine 3 DISCH 1 <DISCH> [K4 Верхний пульт] [Верхний пульт] [01 (Fire Control Panel) Пульт пожарной сигнализации]
	"O10_b03",	# engine 3 DISCH 2 <1> [K4 Верхний пульт] [Верхний пульт] [01 (Fire Control Panel) Пульт пожарной сигнализации]
	"O10_b04",	# engine 3 DISCH 2 <DISCH> [K4 Верхний пульт] [Верхний пульт] [01 (Fire Control Panel) Пульт пожарной сигнализации]
	"O10_b05",	# FIRE REAR COMP DISCH <DISCH> [K4 Верхний пульт] [Верхний пульт] [01 (Fire Control Panel) Пульт пожарной сигнализации]
	"O10_b06",	# FIRE BAG COMP DISCH <DISCH> [K4 Верхний пульт] [Верхний пульт] [01 (Fire Control Panel) Пульт пожарной сигнализации]
	"O10_b07",	# AJB AUTO EXT. <OFF> [K4 Верхний пульт] [Верхний пульт] [02 - 03 FLIGHT CONTROL  - STEERING FL CON]
	"O10_b08",	# FCS ENGAGE NORM <?????> [K4 Верхний пульт] [Верхний пульт] [02 - 03 FLIGHT CONTROL  - STEERING FL CON]
	"O10_b09",	# FCS ENGAGE ST-BY <?????> [K4 Верхний пульт] [Верхний пульт] [02 - 03 FLIGHT CONTROL  - STEERING FL CON]
	"O10_b10",	# NWS <OFF> [K4 Верхний пульт] [Верхний пульт] [02 - 03 FLIGHT CONTROL  - STEERING FL CON]
	"O10_b11",	# APU Master <ON> [K4 Верхний пульт] [Верхний пульт] [04 - 05 - 06 Engines Manual Start - APU control panel - HYDROLYCS]
	"O10_b12",	# APU Start / Stop <RUN> [K4 Верхний пульт] [Верхний пульт] [04 - 05 - 06 Engines Manual Start - APU control panel - HYDROLYCS]
	"O10_b13",	# SHUT OFF A1 <CLOSE> [K4 Верхний пульт] [Верхний пульт] [04 - 05 - 06 Engines Manual Start - APU control panel - HYDROLYCS]
	"O10_b14",	# SHUT OFF A3 <CLOSE> [K4 Верхний пульт] [Верхний пульт] [04 - 05 - 06 Engines Manual Start - APU control panel - HYDROLYCS]
	"O10_b15",	# SHUT OFF B2 <CLOSE> [K4 Верхний пульт] [Верхний пульт] [04 - 05 - 06 Engines Manual Start - APU control panel - HYDROLYCS]
	"O10_b16",	# SHUT OFF B3 <CLOSE> [K4 Верхний пульт] [Верхний пульт] [04 - 05 - 06 Engines Manual Start - APU control panel - HYDROLYCS]
	"O10_b17",	# SHUT OFF C2 <CLOSE> [K4 Верхний пульт] [Верхний пульт] [04 - 05 - 06 Engines Manual Start - APU control panel - HYDROLYCS]
	"O10_b18",	# BACK UP PUMP <ON> [K4 Верхний пульт] [Верхний пульт] [04 - 05 - 06 Engines Manual Start - APU control panel - HYDROLYCS]
	"O10_b19",	# BACK UP PUMP <OFF> [K4 Верхний пульт] [Верхний пульт] [04 - 05 - 06 Engines Manual Start - APU control panel - HYDROLYCS]
	"O10_b27",	# CABIN MASTER <SHEO> [K4 Верхний пульт] [Верхний пульт] [07 - 09 DC SUPPLY (Electrical System control panel) - ANTI-ICE]
	"O10_b28",	# CABIN MASTER <OFF> [K4 Верхний пульт] [Верхний пульт] [07 - 09 DC SUPPLY (Electrical System control panel) - ANTI-ICE]
	"O10_b29",	# RH MASTER <OFF> [K4 Верхний пульт] [Верхний пульт] [07 - 09 DC SUPPLY (Electrical System control panel) - ANTI-ICE]
	"O10_b30",	# RH INIT <OFF> [K4 Верхний пульт] [Верхний пульт] [07 - 09 DC SUPPLY (Electrical System control panel) - ANTI-ICE]
	"O10_b31",	# BUS TIE <TIED> [K4 Верхний пульт] [Верхний пульт] [07 - 09 DC SUPPLY (Electrical System control panel) - ANTI-ICE]
	"O10_b32",	# LH INIT <OFF> [K4 Верхний пульт] [Верхний пульт] [07 - 09 DC SUPPLY (Electrical System control panel) - ANTI-ICE]
	"O10_c01",	# LH MASTER <OFF> [K4 Верхний пульт] [Верхний пульт] [07 - 09 DC SUPPLY (Electrical System control panel) - ANTI-ICE]
	"O10_c02",	# RH ISOL <ISOL> [K4 Верхний пульт] [Верхний пульт] [07 - 09 DC SUPPLY (Electrical System control panel) - ANTI-ICE]
	"O10_c03",	# GALLEY MASTER <OFF> [K4 Верхний пульт] [Верхний пульт] [07 - 09 DC SUPPLY (Electrical System control panel) - ANTI-ICE]
	"O10_c04",	# GEN 2 <OFF> [K4 Верхний пульт] [Верхний пульт] [07 - 09 DC SUPPLY (Electrical System control panel) - ANTI-ICE]
	"O10_c05",	# GALLEY MASTER <SHEO> [K4 Верхний пульт] [Верхний пульт] [07 - 09 DC SUPPLY (Electrical System control panel) - ANTI-ICE]
	"O10_c06",	# GEN 3 <OFF> [K4 Верхний пульт] [Верхний пульт] [07 - 09 DC SUPPLY (Electrical System control panel) - ANTI-ICE]
	"O10_c07",	# GEN  1 <OFF> [K4 Верхний пульт] [Верхний пульт] [07 - 09 DC SUPPLY (Electrical System control panel) - ANTI-ICE]
	"O10_c08",	# EXT POWER <BUTTON> [K4 Верхний пульт] [Верхний пульт] [07 - 09 DC SUPPLY (Electrical System control panel) - ANTI-ICE]
	"O10_c09",	# LH ISOL <ISOL> [K4 Верхний пульт] [Верхний пульт] [07 - 09 DC SUPPLY (Electrical System control panel) - ANTI-ICE]
	"O10_c10",	# WINGS <ON> [K4 Верхний пульт] [Верхний пульт] [07 - 09 DC SUPPLY (Electrical System control panel) - ANTI-ICE]
	"O10_c11",	# WINGS <ST-BY> [K4 Верхний пульт] [Верхний пульт] [07 - 09 DC SUPPLY (Electrical System control panel) - ANTI-ICE]
	"O10_c12",	# BRAKE <ON> [K4 Верхний пульт] [Верхний пульт] [07 - 09 DC SUPPLY (Electrical System control panel) - ANTI-ICE]
	"O10_c13",	# ENG 1 <ON> [K4 Верхний пульт] [Верхний пульт] [07 - 09 DC SUPPLY (Electrical System control panel) - ANTI-ICE]
	"O10_c14",	# ENG 2 <ON> [K4 Верхний пульт] [Верхний пульт] [07 - 09 DC SUPPLY (Electrical System control panel) - ANTI-ICE]
	"O10_c15",	# ENG 2 <ST-BY> [K4 Верхний пульт] [Верхний пульт] [07 - 09 DC SUPPLY (Electrical System control panel) - ANTI-ICE]
	"O10_c16",	# ENG 3 <ON> [K4 Верхний пульт] [Верхний пульт] [07 - 09 DC SUPPLY (Electrical System control panel) - ANTI-ICE]
	"O10_b24",	# BAG ISOL <OFF> [K4 Верхний пульт] [Верхний пульт] [08 AIR CONDITION - BLEED - Pressurization   Bleed control panel Pressurization control panel]
	"O10_b25",	# XBLEED ECS <OFF> [K4 Верхний пульт] [Верхний пульт] [08 AIR CONDITION - BLEED - Pressurization   Bleed control panel Pressurization control panel]
	"O10_b26",	# XBLEED ECS <ON> [K4 Верхний пульт] [Верхний пульт] [08 AIR CONDITION - BLEED - Pressurization   Bleed control panel Pressurization control panel]
	"O10_b20",	# PAX AFT TEMP <INOP> [K4 Верхний пульт] [Верхний пульт] [08 AIR CONDITION - BLEED - Pressurization   Bleed control panel Pressurization control panel]
	"O10_b21",	# PAX FWD TEMP <MAN> [K4 Верхний пульт] [Верхний пульт] [08 AIR CONDITION - BLEED - Pressurization   Bleed control panel Pressurization control panel]
	"O10_b22",	# CREW TEMP <MAN> [K4 Верхний пульт] [Верхний пульт] [08 AIR CONDITION - BLEED - Pressurization   Bleed control panel Pressurization control panel]
	"O10_b23",	# GND VENT <OFF> [K4 Верхний пульт] [Верхний пульт] [08 AIR CONDITION - BLEED - Pressurization   Bleed control panel Pressurization control panel]
	"O10_c17",	# BLEED 1 <OFF> [K4 Верхний пульт] [Верхний пульт] [08 AIR CONDITION - BLEED - Pressurization   Bleed control panel Pressurization control panel]
	"O10_c18",	# BLEED 1 <HP OFF> [K4 Верхний пульт] [Верхний пульт] [08 AIR CONDITION - BLEED - Pressurization   Bleed control panel Pressurization control panel]
	"O10_c19",	# XBLEED 1--2 <OFF> [K4 Верхний пульт] [Верхний пульт] [08 AIR CONDITION - BLEED - Pressurization   Bleed control panel Pressurization control panel]
	"O10_c20",	# XBLEED 1--2 <ON> [K4 Верхний пульт] [Верхний пульт] [08 AIR CONDITION - BLEED - Pressurization   Bleed control panel Pressurization control panel]
	"O10_c21",	# BLEED 2 <HP OFF> [K4 Верхний пульт] [Верхний пульт] [08 AIR CONDITION - BLEED - Pressurization   Bleed control panel Pressurization control panel]
	"O10_c22",	# BLEED 2 <OFF> [K4 Верхний пульт] [Верхний пульт] [08 AIR CONDITION - BLEED - Pressurization   Bleed control panel Pressurization control panel]
	"O10_c23",	# XBLEED 2--3 <ON> [K4 Верхний пульт] [Верхний пульт] [08 AIR CONDITION - BLEED - Pressurization   Bleed control panel Pressurization control panel]
	"O10_c24",	# XBLEED 2--3 <OFF> [K4 Верхний пульт] [Верхний пульт] [08 AIR CONDITION - BLEED - Pressurization   Bleed control panel Pressurization control panel]
	"O10_c25",	# BLEED APU <ON> [K4 Верхний пульт] [Верхний пульт] [08 AIR CONDITION - BLEED - Pressurization   Bleed control panel Pressurization control panel]
	"O10_c26",	# BLEED APU <OFF> [K4 Верхний пульт] [Верхний пульт] [08 AIR CONDITION - BLEED - Pressurization   Bleed control panel Pressurization control panel]
	"O10_c27",	# BLEED 3 <HP OFF> [K4 Верхний пульт] [Верхний пульт] [08 AIR CONDITION - BLEED - Pressurization   Bleed control panel Pressurization control panel]
	"O10_c28",	# BLEED 3 <OFF> [K4 Верхний пульт] [Верхний пульт] [08 AIR CONDITION - BLEED - Pressurization   Bleed control panel Pressurization control panel]
	"O10_c29",	# DUMP <ON> [K4 Верхний пульт] [Верхний пульт] [08 AIR CONDITION - BLEED - Pressurization   Bleed control panel Pressurization control panel]
	"O10_c30",	# BAG VENT <ON> [K4 Верхний пульт] [Верхний пульт] [08 AIR CONDITION - BLEED - Pressurization   Bleed control panel Pressurization control panel]
	"O10_c31",	# BAG VENT <OFF> [K4 Верхний пульт] [Верхний пульт] [08 AIR CONDITION - BLEED - Pressurization   Bleed control panel Pressurization control panel]
	"O10_c32",	# PRESSU MAN <ON> [K4 Верхний пульт] [Верхний пульт] [08 AIR CONDITION - BLEED - Pressurization   Bleed control panel Pressurization control panel]
	"O11_a10",	# BOOST 1 <OFF> [K4 Верхний пульт] [Верхний пульт] [10 Fuel System control panel]
	"O11_a11",	# BOOST 1 <ST-BY> [K4 Верхний пульт] [Верхний пульт] [10 Fuel System control panel]
	"O11_a12",	# BOOST 2 <OFF> [K4 Верхний пульт] [Верхний пульт] [10 Fuel System control panel]
	"O11_a13",	# BOOST 2 <ST-BY> [K4 Верхний пульт] [Верхний пульт] [10 Fuel System control panel]
	"O11_a14",	# BOOST 3 <OFF> [K4 Верхний пульт] [Верхний пульт] [10 Fuel System control panel]
	"O11_a15",	# RH MASTER <OFF> [K4 Верхний пульт] [Верхний пульт] [10 Fuel System control panel]
	"O11_a16",	# BOOST 3 <ST-BY> [K4 Верхний пульт] [Верхний пульт] [10 Fuel System control panel]
	"O11_a17",	# X-BP 1<-->2  <ON> [K4 Верхний пульт] [Верхний пульт] [10 Fuel System control panel]
	"O11_a18",	# X-BP 1<-->3  <ON> [K4 Верхний пульт] [Верхний пульт] [10 Fuel System control panel]
	"O11_a19",	# X-BP 2<-->3  <ON> [K4 Верхний пульт] [Верхний пульт] [10 Fuel System control panel]
	"O11_a20",	# XTK DOWN 1  <ON> [K4 Верхний пульт] [Верхний пульт] [10 Fuel System control panel]
	"O11_a21",	# XTK DOWN 2  <ON> [K4 Верхний пульт] [Верхний пульт] [10 Fuel System control panel]
	"O11_a22",	# XTK LEFT 1  <ON> [K4 Верхний пульт] [Верхний пульт] [10 Fuel System control panel]
	"O11_a23",	# XTK RIGHT 1  <ON> [K4 Верхний пульт] [Верхний пульт] [10 Fuel System control panel]
	"O11_a24",	# XTK UP 1  <ON> [K4 Верхний пульт] [Верхний пульт] [10 Fuel System control panel]
	"O11_a25",	# XTK UP 2  <ON> [K4 Верхний пульт] [Верхний пульт] [10 Fuel System control panel]
	"O11_a01",	# PROBE 1+2 <OFF> [K4 Верхний пульт] [Верхний пульт] [11 - 12 - 13 WINDSHEILD HEAT - PILOT HEAT - PAX OXYGEN]
	"O11_a02",	# PROBE 3 <OFF> [K4 Верхний пульт] [Верхний пульт] [11 - 12 - 13 WINDSHEILD HEAT - PILOT HEAT - PAX OXYGEN]
	"O11_a03",	# PROBE 4 <OFF> [K4 Верхний пульт] [Верхний пульт] [11 - 12 - 13 WINDSHEILD HEAT - PILOT HEAT - PAX OXYGEN]
	"O11_a04",	# LH <OFF> [K4 Верхний пульт] [Верхний пульт] [11 - 12 - 13 WINDSHEILD HEAT - PILOT HEAT - PAX OXYGEN]
	"O11_a05",	# LH <MAX> [K4 Верхний пульт] [Верхний пульт] [11 - 12 - 13 WINDSHEILD HEAT - PILOT HEAT - PAX OXYGEN]
	"O11_a06",	# RH <OFF> [K4 Верхний пульт] [Верхний пульт] [11 - 12 - 13 WINDSHEILD HEAT - PILOT HEAT - PAX OXYGEN]
	"O11_a07",	# RH <MAX> [K4 Верхний пульт] [Верхний пульт] [11 - 12 - 13 WINDSHEILD HEAT - PILOT HEAT - PAX OXYGEN]
	"O11_a08",	# BACK UP <MAX LH> [K4 Верхний пульт] [Верхний пульт] [11 - 12 - 13 WINDSHEILD HEAT - PILOT HEAT - PAX OXYGEN]
	"O11_a09",	# BACK UP  <MAX RH> [K4 Верхний пульт] [Верхний пульт] [11 - 12 - 13 WINDSHEILD HEAT - PILOT HEAT - PAX OXYGEN]
	"O11_a26",	# NAV <LOGO> [K4 Верхний пульт] [Верхний пульт] [15 EXTERIOR LIGHTS + RAIN RPLNT LH]
	"O11_a27",	# NAV <OFF> [K4 Верхний пульт] [Верхний пульт] [15 EXTERIOR LIGHTS + RAIN RPLNT LH]
	"O11_a28",	# ANTICOL <OFF> [K4 Верхний пульт] [Верхний пульт] [15 EXTERIOR LIGHTS + RAIN RPLNT LH]
	"O11_a29",	# ANTICOL <RED> [K4 Верхний пульт] [Верхний пульт] [15 EXTERIOR LIGHTS + RAIN RPLNT LH]
	"O11_a30",	# WINGS <OFF> [K4 Верхний пульт] [Верхний пульт] [15 EXTERIOR LIGHTS + RAIN RPLNT LH]
	"O11_a31",	# TAXI <ON> [K4 Верхний пульт] [Верхний пульт] [15 EXTERIOR LIGHTS + RAIN RPLNT LH]
	"O11_a32",	# SWITCH LANDING 1 <LDG> [K4 Верхний пульт] [Верхний пульт] [15 EXTERIOR LIGHTS + RAIN RPLNT LH]
	"O11_b01",	# SWITCH LANDING 2 <LDG> [K4 Верхний пульт] [Верхний пульт] [15 EXTERIOR LIGHTS + RAIN RPLNT LH]
	"O11_b02",	# CABIN <PAX> [K4 Верхний пульт] [Верхний пульт] [16 - 17 COCKPIT LIGHTS - INTERIOR LIGHTS + RAIN RPLNT RH]
	"O11_b03",	# FASTEN BELT <ON> [K4 Верхний пульт] [Верхний пульт] [16 - 17 COCKPIT LIGHTS - INTERIOR LIGHTS + RAIN RPLNT RH]
	"O11_b04",	# NO SMOKING <ON> [K4 Верхний пульт] [Верхний пульт] [16 - 17 COCKPIT LIGHTS - INTERIOR LIGHTS + RAIN RPLNT RH]
	"O11_b05",	# CABIN <OFF> [K4 Верхний пульт] [Верхний пульт] [16 - 17 COCKPIT LIGHTS - INTERIOR LIGHTS + RAIN RPLNT RH]
	"O11_b06",	# SWITCH <EMERG LIGHTS> [K4 Верхний пульт] [Верхний пульт] [16 - 17 COCKPIT LIGHTS - INTERIOR LIGHTS + RAIN RPLNT RH]
    "O11_b07",	# engine 1 shut off FIRE <red light> [K4 Верхний пульт] [Верхний пульт] [16 - 17 COCKPIT LIGHTS - INTERIOR LIGHTS + RAIN RPLNT RH]
	"O11_b08",	# FIRE APU <red light> [K4 Верхний пульт] [Верхний пульт] [16 - 17 COCKPIT LIGHTS - INTERIOR LIGHTS + RAIN RPLNT RH]
	"O11_b09",	# engine 2 shut off FIRE 2 <red light> [K4 Верхний пульт] [Верхний пульт] [16 - 17 COCKPIT LIGHTS - INTERIOR LIGHTS + RAIN RPLNT RH]
	"O11_b10",	# FIRE REAR COMP DISCH <red light> [K4 Верхний пульт] [Верхний пульт] [16 - 17 COCKPIT LIGHTS - INTERIOR LIGHTS + RAIN RPLNT RH]
	"O11_b11",	# FIRE BAG COMP DISCH <red light> [K4 Верхний пульт] [Верхний пульт] [16 - 17 COCKPIT LIGHTS - INTERIOR LIGHTS + RAIN RPLNT RH]
	"O11_b12",	# engine 3 shut off FIRE 3 <red light> [K4 Верхний пульт] [Верхний пульт] [16 - 17 COCKPIT LIGHTS - INTERIOR LIGHTS + RAIN RPLNT RH]
]
    
uso_dtype = np.dtype(
    {
        'names': [
            *uso_float_field_names,

            'bitfield',

            "audio_union", # Платa AUDIO
            "toARINC",   # Слова ARINC
            "pDataReady",  # Готовность данных (shared memory)
        ], 

        # https:#numpy.org/doc/stable/reference/arrays.dtypes.html
        'formats': [
            # float fields in uso packet
            *['f4'] * len(uso_float_field_names),

            # bytes occupied by bitfield in uso packet
            ('B', (math.ceil(len(uso_bitfield_names) / 8),)),

            # Платa AUDIO
            # union { ...
            ('u2', (16,)),

            # unsigned int toARINC[20];
            ('i', (20,)),

            # char pDataReady
            'b'
        ]
    }
)
