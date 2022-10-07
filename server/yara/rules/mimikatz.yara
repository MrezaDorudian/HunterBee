rule mimikatz_main {
    strings:
        $exe_x86_1 = { 89 71 04 89 [0-3] 30 8d 04 bd }
        $exe_x86_2 = { 89 79 04 89 [0-3] 38 8d 04 b5 }

        $exe_x64_1 = { 4c 03 d8 49 [0-3] 8b 03 48 89 }
        $exe_x64_2 = { 4c 8b df 49 [0-3] c1 e3 04 48 [0-3] 8b cb 4c 03 [0-3] d8 }

        $dll_1 = {    c7 0? 00 00 01 00 [4-14] c7 0? 01 00 00 00 }
        $dll_2 = { c7 0? 10 02 00 00 ?? 89 4? }

        $sys_x86 = { a0 00 00 00 24 02 00 00 40 00 00 00 [0-4] b8 00 00 00 6c 02 00 00 40 00 00 00 }
        $sys_x64 = { 88 01 00 00 3c 04 00 00 40 00 00 00 [0-4] e8 02 00 00 f8 02 00 00 40 00 00 00 }

    condition:
        (all of ($exe_x86_*)) or (all of ($exe_x64_*)) or (all of ($dll_*)) or (any of ($sys_*))
}

rule mimikatz_sekurlsa {
    strings:
        $s1 = { 33 DB 8B C3 48 83 C4 20 5B C3 }
        $s2 = {83 64 24 30 00 44 8B 4C 24 48 48 8B 0D}
        $s3 = {83 64 24 30 00 44 8B 4D D8 48 8B 0D}
        $s4 = {84 C0 74 44 6A 08 68}
        $s5 = {8B F0 3B F3 7C 2C 6A 02 6A 10 68}
        $s6 = {8B F0 85 F6 78 2A 6A 02 6A 10 68}

    condition:
        all of them
}

rule mimikatz_decryptkeysign {
    strings:
        $s1 = { F6 C2 07 0F 85 0D 1A 02 00 }
        $s2 = { F6 C2 07 0F 85 72 EA 01 00 }
        $s3 = { 4C 8B CB 48 89 44 24 30}
        $s4 = { 4c 89 1b 48 89 43 08 49 89 5b 08 48 8d }

    condition:
        3 of them
}

rule mimikatz_lsass_mdmp {
    strings:
        $lsass = "System32\\lsass.exe"

    condition:
        (uint32(0) == 0x504d444d) and $lsass
}


rule lsadump{
	strings:
		$str_sam_inc	= "\\Domains\\Account" ascii nocase
		$str_sam_exc	= "\\Domains\\Account\\Users\\Names\\" ascii nocase
		$hex_api_call	= {(41 b8 | 68) 00 00 00 02 [0-64] (68 | ba) ff 07 0f 00 }
		$str_msv_lsa	= { 4c 53 41 53 52 56 2e 44 4c 4c 00 [0-32] 6d 73 76 31 5f 30 2e 64 6c 6c 00 }
		$hex_bkey		= { 4b 53 53 4d [20-70] 05 00 01 00}

	condition:
		($str_sam_inc and not $str_sam_exc) or $hex_api_call or $str_msv_lsa or $hex_bkey
}


rule mimikatz_kirbi_ticket {
    strings:
        $asn1 = { 76 82 ?? ?? 30 82 ?? ?? a0 03 02 01 05 a1 03 02 01 16 }

    condition:
        $asn1 at 0
}

rule test {
    strings:
        $asn1 = "sag"

    condition:
        $asn1
}