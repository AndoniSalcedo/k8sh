from pyparsing import (
    Word,
    alphas,
    Optional,
    oneOf,
    Group,
    ZeroOrMore,
    Literal,
    Combine,
    alphanums,
    NotAny,
    White
)

from constants import (
    k8s_all_verbs,
    k8s_verbs,
    k8s_verbs_name,
    k8s_verbs_resource_name,
)

from api_service import get_api_resources

verbs_all = oneOf(" ".join(k8s_all_verbs))
verbs = oneOf(" ".join(k8s_verbs))
verbs_name = oneOf(" ".join(k8s_verbs_name))
verbs_resource_name = oneOf(" ".join(k8s_verbs_resource_name))

name = Word(alphas, alphanums + "-_")

resource = oneOf(" ".join(get_api_resources()))

sortFlagKey = Combine(Literal("-") + Word(alphas, exact=1))
longFlagKey = Combine(Literal("--") + Word(alphanums + "-"))

flagKey = sortFlagKey | longFlagKey
flagValue = Word(alphas, alphanums + "-_")

flag = Group(flagKey + Optional(flagValue))

verb_resource_name = (
    verbs_resource_name("resource")
    + ZeroOrMore(flag("resource"))  
    + Optional(resource("name flags") + Optional(name("flags")))
    + ZeroOrMore(flag("flags"))
)

verb_name = verbs_name("name") + ZeroOrMore(flag)("name") + Optional(name("flags")) + ZeroOrMore(flag)

kubectlCommand = verb_resource_name | verb_name

typeCommand = resource("resource")

flagCommand = flag("flag")

