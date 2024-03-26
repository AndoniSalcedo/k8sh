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

name = Word(alphanums + "-_")

resource = oneOf(" ".join(get_api_resources()))
not_resource = NotAny(resource) + name

flagKeyword = Combine(Literal("-") + Word(alphas, exact=1)) | Combine(
    Literal("--") + Word(alphanums + "-")
)
flagValue = Combine(Word(alphanums, exact=1) + Optional(Word(alphanums + "-_.:/")))
flag = Group(flagKeyword + Optional(flagValue))

verb_resouce_name = (
    verbs_resource_name("resource")
    + Optional(resource("name flags") + Optional(name("flags")))
    + ZeroOrMore(flag("flags"))
)

verb_name = verbs_name("name flags") + Optional(name("flags")) + ZeroOrMore(flag)

kubectlCommand = verb_resouce_name | verb_name

typeCommand = resource("resource") | not_resource

flagCommand = flag("flag") | NotAny(flag)

