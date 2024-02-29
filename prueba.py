from pyparsing import (
    Word,
    Optional,
    oneOf,
    ParseException,
    alphanums,
)
from pyparsing import And, Or, Each, Optional, ZeroOrMore, OneOrMore, NotAny, SkipTo, Token



# Defining the grammar components
verb = oneOf("get logs").setName("verb")
resource = oneOf("pod deployment").setName("resource")
name = Word(alphanums + "-_").setName("name")

# Defining command grammars
kubectlGetCommand = (verb("verb") + resource("resource") + Optional(name)("name")).setName("verb resource name")
kubectlLogsCommand = (verb("verb") + Optional(name)("name")).setName("logs command")

# Unified command grammar
kubectlCommand = kubectlGetCommand | kubectlLogsCommand

print(kubectlCommand)

# Autocompletion suggestion map based on the last parsed element's name
suggestions_map = {
    "verb": ["pod", "deployment"],
    "resource": ["<name>"],
    "name": [],
}

test_inputs = ["get ", "get pod ", "logs "]


for input_text in test_inputs:
    try:
        # Attempt parsing the input text
        
        parsed = kubectlCommand.parseString(input_text, parseAll=True)
        
        for key in parsed.keys():
            print(key)
        print(f"Parsed successfully: {parsed.dump()}")
        print(parsed.asList())
    #suggestions_map[parsed.dump()]
    except ParseException as pe:
        # Parsing failed, indicating incomplete input
        # Use the exception's location to find the last successfully parsed token
        last_token = input_text[:pe.loc].strip().split()[-1]
        # Attempt to re-parse up to the failure point to identify the last token type
        try:
            partial_parsed = kubectlCommand.parseString(input_text[:pe.loc], parseAll=False)
            # Determine the name of the last parsed element
            last_element_name = partial_parsed[-1].getName()
            # Return suggestions based on the last element's name
 
        except ParseException:
            ''''''
        # If re-parsing the partial input also fails, suggest starting options