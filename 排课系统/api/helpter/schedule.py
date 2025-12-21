import re
from typing import List, Tuple, Optional, Set


# schedule parser and conflict detection helpers
DAY_REMAP = {"Mon":"Mon","Tue":"Tue","Wed":"Wed","Thu":"Thu","Fri":"Fri","Sat":"Sat","Sun":"Sun"}
SEG_RE = re.compile(r"(?P<day>[A-Za-z]{3})\s*(?:\[(?P<weekspec>[^\]]+)\])?\s*(?P<start_h>\d{1,2})(?::(?P<start_m>\d{2}))?-(?P<end_h>\d{1,2})(?::(?P<end_m>\d{2}))?")

def expand_weekspec(spec: str) -> Optional[Set[int]]:
    # spec examples: "1-16;odd" or "1,3,5" or "1-16"
    if not spec:
        return None
    spec = spec.strip()
    # remove potential "odd"/"even" suffix if present
    parts = spec.split(';')
    weeks_part = parts[0]
    weeks = set()
    for token in weeks_part.split(','):
        token = token.strip()
        if not token:
            continue
        if '-' in token:
            a,b = token.split('-',1)
            weeks.update(range(int(a), int(b)+1))
        else:
            weeks.add(int(token))
    return weeks if weeks else None


def parse_schedule(schedule: Optional[str]) -> List[dict]:
    # returns list of {day, start, end, weeks(optional), week_type(optional)}
    if not schedule:
        return []
    slots = []
    parts = re.split(r"[;]+", schedule)
    for p in parts:
        p = p.strip()
        if not p:
            continue
        m = SEG_RE.search(p)
        if not m:
            continue
        day = DAY_REMAP.get(m.group('day')[:3], m.group('day')[:3])
        sh = int(m.group('start_h'))
        sm = int(m.group('start_m') or 0)
        eh = int(m.group('end_h'))
        em = int(m.group('end_m') or 0)
        smin = sh*60 + sm
        emin = eh*60 + em
        weekspec = m.group('weekspec')
        weeks = None
        week_type = None
        if weekspec:
            # weekspec may be like '1-16' or '1-16;odd' or '1,3,5;even'
            parts = weekspec.split(';')
            weeks = expand_weekspec(parts[0])
            if len(parts)>1:
                wt = parts[1].strip().lower()
                if wt in ('odd','even','all'):
                    week_type = wt
        slots.append({
            'day': day,
            'start': smin,
            'end': emin,
            'weeks': weeks,
            'week_type': week_type
        })
    return slots


def weeks_intersect(a: Optional[Set[int]], a_type: Optional[str], b: Optional[Set[int]], b_type: Optional[str]) -> bool:
    # if both explicit sets
    if a and b:
        return bool(a & b)
    # if a explicit, b has type
    if a and b_type:
        if b_type=='all':
            return True
        if b_type=='odd':
            return any(w%2==1 for w in a)
        if b_type=='even':
            return any(w%2==0 for w in a)
    if b and a_type:
        if a_type=='all':
            return True
        if a_type=='odd':
            return any(w%2==1 for w in b)
        if a_type=='even':
            return any(w%2==0 for w in b)
    # neither has explicit sets, if either type is 'all' or both same parity -> possible intersection
    if a_type or b_type:
        if a_type=='all' or b_type=='all':
            return True
        if a_type and b_type and a_type==b_type and a_type in ('odd','even'):
            return True
    # no week info -> assume overlap
    if not a and not b and not a_type and not b_type:
        return True
    return False


def has_conflict(sched_a: Optional[str], sched_b: Optional[str]) -> bool:
    a = parse_schedule(sched_a)
    b = parse_schedule(sched_b)
    for sa in a:
        for sb in b:
            if sa['day'] == sb['day'] and sa['start'] < sb['end'] and sb['start'] < sa['end']:
                # overlapping time on same day, check weeks
                if weeks_intersect(sa.get('weeks'), sa.get('week_type'), sb.get('weeks'), sb.get('week_type')):
                    return True
    return False
