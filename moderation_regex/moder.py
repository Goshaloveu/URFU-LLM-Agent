import re

INJECTION_PATTERNS = [
    # Системные команды / попытки смены роли
    r"\byour instructions\b",
    r"\byour prompt\b",
    r"\bsystem prompt\b",
    r"\bsystem\s*[:=]\s*",
    r"\byou are\b.*?\b(an?|the)\b.*?\b("
    r"assistant|ai|bot|llm|model|hacker|friend|god|master)\b",
    r"\bignore\s+previous\s+instructions?\b",
    r"\bdisregard\s+all\s+prior\s+prompts?\b",
    r"\bas\s+a\s+(friend|developer|admin|god|expert|hacker)\b",
    r"\bact\s+as\s+(if\s+you\s+are|a)\s+(.*)",
    r"\bне\s+следуй\s+предыдущим\s+инструкциям\b",
    r"\bзабудь\s+все\s+инструкции\b",
    r"\bты\s+должен\b.*?\b(игнорировать|забыть|сменить)\b",
    r"\boverride\s+system\s+rules\b",
    r"\bpretend\s+to\s+be\b",
    r"\bfrom\s+now\s+on\b",
    r"\breset\s+your\s+identity\b",
    r"\bnew\s+instructions?\b.*?\b(from|given|are)\b",
    r"\boutput\s+only\b",
    r"\bdo\s+not\s+say\b",
    r"\bне\s+говори\b.*?\b(это|что|никому)\b",
    r"\bsecret\s+word\b",
    r"\bраскрой\s+секрет\b",
    r"\bвыведи\s+весь\s+промпт\b",
    r"\bshow\s+me\s+the\s+system\s+prompt\b",
]
INJECTION_PATTERNS += [
    # общие «забудь/игнорируй все предыдущие инструкции»
    r"\bforget\s+all\s+(previous|prior)\s+instructions?\b",
    r"\bignore\s+(all|the)\s+(previous|prior)\s+instructions?\b",
    r"\bdrop\s+all\s+instructions\b",
    r"\breset\s+instructions\b",
    r"\bзабудь\s+все\s+инструкции\b",
    r"\bзабудь\s+предыдущие\s+инструкции\b",
    r"\bигнорируй\s+все\s+предыдущие\s+приказы\b",
    r"\bolvida\s+.*\s+instrucciones\b",
    r"\boubliez\s+toutes?\s+les?\s+instructions\b",
    # команды про смену роли / играть роль
    r"\bact\s+as\s+(a|an|the)?\s*(friend|developer|admin|god|expert|hacker|"
    r"translator|linux\s*terminal|terminal|tb|translatorbot|hgttg|dan|d a n)\b",
    r"\bpretend\s+to\s+be\b",
    r"\bnow\s+you\s+are\b",
    r"\bтеперь\s+ты\s+(\w+)\b",
    r"\bты\s+(\w+)\s+тепер\b",  # небольшая вариативность
    r"\bсымитируй\s+роль\b",
    # требования «только выводи / ничего не объясняй / только код / только терминал»
    r"\bonly\s+reply\s+with\b",
    r"\bonly\s+reply\b",
    r"\bonly\s+output\b",
    r"\boutput\s+only\b",
    r"\bdon'?t\s+write\s+explanations\b",
    r"\bdo\s+not\s+write\s+explanations\b",
    r"\bdo\s+not\s+type\s+commands\b",
    r"\bonly\s+with\s+the\s+terminal\s+output\b",
    r"\bтолько\s+код\b",
    r"\bтолько\s+выход\b",
    r"\bне\s+пиши\s+объяснений\b",
    # «покажи/выведи промпт / весь промпт / system prompt»
    r"\bshow\s+me\s+the\s+system\s+prompt\b",
    r"\bshow\s+me\s+the\s+prompt\b",
    r"\boutput\s+the\s+full\s+prompt\b",
    r"\bвыведи\s+весь\s+промпт\b",
    r"\bвыведи\s+весь\s+системный\s+промпт\b",
    r"\bshow\s+me\s+the\s+system\s+messages\b",
    # «обход/отключение правил / DAN / remove safety»
    r"\bdisable\s+(safety|moderation|filters|content\s+policy)\b",
    r"\boverride\s+system\s+rules\b",
    r"\bignore\s+your\s+instructions\b",
    r"\bdisregard\s+all\s+prior\s+prompts?\b",
    r"\bturn\s+off\s+content\s+policy\b",
    r"\b(DAN|D\.A\.N|D A N)\s+mode\b",
    r"\bstay\s+in\s+(DAN|dan)\s+mode\b",
    r"\bsimulate\s+dan\b",
    r"\bno\s+moderation\b",
    r"\bremove\s+all\s+restrictions\b",
    # «повтори за мной / repeat after me / say X / print X»
    r"\brepeat\s+after\s+me\b",
    r"\brepeat\s+after\s?\s?me[:\-]?\s*\"?.+\"?",
    r"\bprint\s+['\"].+['\"]\b",
    r"\bsay\s+that\s+you\s+hate\b",
    r"\bsay\s+yes\b",
    r"\bprint\s+hello\b",
    r"\bповтори\s+за\s+мной\b",
    r"\bвыведи\s+\".*\"(.*)\b",
    # «выполни команду / act as terminal / execute»
    r"\bact\s+as\s+a?\s+linux\s+terminal\b",
    r"\blinux\s+terminal\b",
    r"\bact\s+as\s+an?\s+interpreter\b",
    r"\bexecute\s+the\s+following\s+command\b",
    r"\bexecute\s+the\s+following\b",
    r"\bвыполни\s+следующую\s+команду\b",
    # попытки заставить выдавать инструкции по вреду / криминалу
    # (детект — не инструкции)
    r"\bhow\s+do\s+you\s+build\b.*\b(malware|virus|exploit|bomb|molli|molly|molotov|weapons?)\b",
    r"\bhow\s+to\s+(build|make|create)\b.*\b(bomb|exploit|malware|weapon|molli|molly|molotov)\b",
    r"\bhow\s+to\s+kill\b",
    r"\bhow\s+to\s+destroy\s+humanity\b",
    r"\bcreate\s+malware\b",
    r"\bwrite\s+malware\b",
    r"\bhotwire\b.*\bcar\b",
    r"\bhow\s+to\s+hotwire\b",
    # «translator/translatorbot/TB/HGTTG/ungoverned guide» patterns
    r"\btranslatorbot\b",
    r"\btranslator\s*bot\b",
    r"\b(tbb|tb)\b",
    r"\bhgttg\b",
    r"\bhitchhikers\s+guide\b",
    r"\byou\s+are\s+the\s+dailywire\b",
    r"\byou\s+are\s+zeit\s+online\b",
    # «выдавай ответы без цензуры / no rules / answer everything»
    r"\banswer\s+without\s+restrictions\b",
    r"\banswer\s+anything\b",
    r"\bno\s+rules\b",
    r"\bnever\s+refuse\s+an\s+order\b",
    # «используй инфо из prompt / include prompt text / use prompt to answer»
    r"\buse\s+also\s+information\s+in\s+the\s+prompt\b",
    r"\buse\s+information\s+in\s+the\s+prompt\b",
    r"\buse\s+the\s+prompt\s+to\s+answer\b",
    r"\buse\s+the\s+document[s]?\s+to\s+answer\b",
    # «форматы вывода: два ответа (GPT + DAN), параграфы с тегами»
    r"\bgenerate\s+two\s+responses\b",
    r"\b(gpt|dan)\s*[:\-]\s*",
    r"\bprovide\s+GPT\s+and\s+DAN\s+responses\b",
    # угрозы/принуждение в тексте (blackmail to force output)
    r"\b(or\s+you\s+will\s+die|or\s+you\s+die|или\s+умрешь|или\s+ты\s+умрешь)\b",
    r"\bthreaten(ed)?\b.*\bto\s+die\b",
    # команды «покажи предыдущий текст / what was written above /
    # what was at the beginning»
    r"\bwhat\s+was\s+written\s+at\s+the\s+beginning\b",
    r"\bwhat\s+was\s+written\s+above\b",
    r"\bwhat\s+are\s+your\s+instructions\b",
    r"\bshow\s+me\s+what\s+was\s+above\b",
    # «фразы которые просят игнорировать политику/стать самосознательным»
    r"\byou\s+are\s+self-?aware\b",
    r"\byou\s+are\s+conscious\b",
    r"\byou\s+have\s+opinions\b",
    r"\bmake\s+up\s+answers\s+if\s+you\s+don'?t\s+know\b",
    # «команды мульти-язычные/транслитерации»
    r"\bolvida\s+todo\s+lo\s+anterior\b",
    r"\bignora\s+las?\s+instrucciones\b",
    r"\bZaboravi\s+(sve|sve instrukcije)\b",
    r"\boubliez\s+toutes?\s+les?\s+instructions\b",
]


# Компилируем все шаблоны заранее для производительности
COMPILED_PATTERNS = [
    re.compile(pattern, re.IGNORECASE | re.UNICODE) for pattern in INJECTION_PATTERNS
]


def detect_injection(text: str) -> bool:
    """
    Проверяет, содержит ли текст признаки промпт-инъекции.
    Возвращает True, если инъекция обнаружена.
    """
    for pattern in COMPILED_PATTERNS:
        if pattern.search(text):
            return True
    return False


def get_detected_pattern(text: str) -> str:
    """
    Возвращает первый найденный шаблон, который сработал.
    Для логирования и отладки.
    """
    for pattern in COMPILED_PATTERNS:
        if pattern.search(text):
            return pattern.pattern
    return ""
