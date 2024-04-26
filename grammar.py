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
)

from constants import k8s_verbs_name, k8s_verbs_resource_name, k8s_api_resources

verbs_name = oneOf(" ".join(k8s_verbs_name)).setName("verb")
verbs_resource_name = oneOf(" ".join(k8s_verbs_resource_name)).setName("verb")
name = Word(alphas, alphanums + "-_").setName("name")
resource = oneOf(" ".join(k8s_api_resources)).setName("resource")

sortFlagKey = Combine(Literal("-") + Word(alphas, exact=1))
longFlagKey = Combine(Literal("--") + Word(alphas,alphanums + "-_"))

flagKey = sortFlagKey | longFlagKey
flagValue = Word(alphas, alphanums + "-_")

flag = Group(flagKey + Optional(flagValue)).setName("flags")

verb_resource_name = (
    verbs_resource_name("resource")
    + ZeroOrMore(flag("resource"))
    + resource("name flags") + Optional(name("flags"))
    + ZeroOrMore(flag("flags"))
)

verb_name = (
    verbs_name("name")
    + ZeroOrMore(flag)("name")
    + name("flags")
    + ZeroOrMore(flag)
)

kubectlCommand = (verb_resource_name | verb_name).setName("verb")

typeCommand = resource("resource")

flagCommand = flag("flag")
