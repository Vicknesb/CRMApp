import os, re, glob

tickets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..', 'tickets')
tickets_dir = os.path.normpath(tickets_dir)

prefix_map = {
    'PLAT':'plat','DB':'db','AUTH':'auth','LEAD':'lead','CONT':'cont',
    'ACCT':'acct','PIPE':'pipe','ACTV':'actv','TICK':'tick','SLA':'sla',
    'KB':'kb','PROJ':'proj','CONTR':'contr','INV':'inv','CAMP':'camp',
    'ANLY':'anly','COMM':'comm','ADMN':'admn','INTG':'intg','DATA':'data',
    'NFR':'nfr','VERIFY':'verify','SEED':'seed'
}

epic_files = glob.glob(os.path.join(tickets_dir, 'epic-*.md'))
total = 0

for epic_file in epic_files:
    with open(epic_file, encoding='utf-8') as f:
        raw = f.read()

    header_match = re.match(r'^(.*?)(?=\n###\s)', raw, re.DOTALL)
    epic_header = header_match.group(1).strip() if header_match else ''
    epic_oneliner = ''
    for line in epic_header.split('\n'):
        clean = line.strip().lstrip('#').strip()
        if clean:
            epic_oneliner = clean
            break

    parts = re.split(r'(?m)^(?=###\s+[A-Z]+-\d+)', raw)

    for block in parts:
        block = block.strip()
        if not block:
            continue
        id_match = re.match(r'^###\s+([A-Z]+-\d+)\b', block)
        if not id_match:
            continue
        ticket_id = id_match.group(1)
        prefix = re.match(r'^([A-Z]+)', ticket_id).group(1)

        if prefix not in prefix_map:
            print(f'  WARNING: unknown prefix {prefix} ({ticket_id}) -- skipping')
            continue

        sub_dir = os.path.join(tickets_dir, prefix_map[prefix])
        os.makedirs(sub_dir, exist_ok=True)

        banner = f'> **Epic context:** {epic_oneliner}\n\n' if epic_oneliner else ''
        out_path = os.path.join(sub_dir, f'{ticket_id}.md')
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(banner + block)
        total += 1

print(f'Done. {total} ticket files written to tickets/PREFIX/ subfolders.')
