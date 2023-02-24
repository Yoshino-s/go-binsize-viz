import re

undefined_re=re.compile(r'^\s*(\d+)\s+U\s+',re.A)
entries_re=re.compile(r'^\s*([0-9a-fA-F]+)\s+(\d+)\s+(\S+)\s+(.*)$',re.A)
template_part=r'''<(?:[^<>]|(?:<(?:[^<>]|(?:<(?:[^<>]|(?:<(?:[^<>]|(?:<(?:[^<>]|(?:<(?:[^<>]|(?:<(?:[^<>]|(?:<(?:[^<>]|(?:<[^<>]*>))*>))*>))*>))*>))*>))*>))*>))*>'''
parengroup=template_part.replace("<",r'\(').replace(">",r'\)')
cpp_path=r'''(?:\([^)]*\)|\{[^}]*\}|~?(?:\$?\w+|operator(?:[^\(]+|\(\)))(?:'''+template_part+''')?(?:'''+parengroup+r''')?(?:\sconst)?)::|[a-zA-Z]+_'''
cpp_path_re=re.compile(cpp_path,re.X|re.A)
cpp_sym_re=re.compile(r'''^(?:guard\svariable\sfor\s)?((?:(?:\w|::|-|\*|\&|(?:'''+template_part+r'''))+\s)*)((?:'''+cpp_path+r''')*)(\{[^}]*\}|~?(?:\$?\w+|operator(?:[^\(]+|\(\))|\._\d+)(?:\[[^][]*\])?(?:'''+template_part+''')?(?:'''+parengroup+r'''(?:\sconst)?(?:\s\[.*\])?(?:\s\((?:\.(?:constprop|part|isra).\d+)+\))?)?(?:\*+)?)$''',re.X|re.A)
go_path_parts=r'''\((?:[^()]|\([^()]*\))*\)\.|struct\s\{(?:[^{}]|\{[^{}]*\})*\}\.|\$?(?:\w|-|%)+\.|glob\.\.|time\.\.|\.gobytes\.|\.dict\.|(?:\w|\.|-|%)+\/'''
go_path_parts_re=re.compile(go_path_parts,re.X|re.A)
go_last_part=r'''(?:(?:\.?(?:(?:\w|-|%)+(?:\[.+\])?|\([^()]*\))(?:-fm)?)|struct\s\{(?:[^{}]|\{[^{}]*\})*\})(?:,(?:(?:(?:\w|\.|-|%)+\/)*(?:\w|-|%|\.)+|interface\s\{(?:[^{}]|\{[^{}]*\})*\}))?|initdone\.|initdone·|\*'''
go_sym_re=re.compile(fr'''^((?:go:(?:itab\.\*?)?)?)((?:{go_path_parts})*)({go_last_part})$''',re.X|re.A)
