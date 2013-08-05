# Mezzo

## Interpreter-Agnostic Script Notation

Mezzo is the least clever programming language possible. It’s a reductive JSON representation of a constrained set of 9 distinct **programming gestures**, as well as a state machine of a program’s current object space. It’s designed to be interpreted, compiled, and operated on asynchronously by client and server-side programs written in Ruby, Python, Javascript, whatever -- Mezzo really doesn't care. By constraining the number of different of different lexical and syntactic concepts available and confining the program to a **state-based, procedural** structure, we eliminate abstract syntax patterns that translate ambiguously in other scripting languages. You could write Mezzo programs and have them interpreted in Python, Ruby or Javascript. Or you could write Python, Ruby or Javascript and have it converted to Mezzo. Or you could write a Mezzo wrapper for most any scripting language. Mezzo doesn’t care.

### Basics

**Base Template** 
```json
{
‘state’: {
“some_name”: {
“type”: ”a primative”,
“value”: value
}
}
“gestures”: [ 
  {“type”: “a directive type”, … },
		… ]
}
```

**State Namespaces** 

State namespaces are objects and they can be nested. They function
as pathed namespaces, rather than one giant global namespace.


```json
{“an object”: {“a nested object”: “attribute name”}}
```

**Primitives**

Mezzo support only JSON primitives.

### Gestures

Mezzo is constrained to a very limited vocabulary of programming ideas that have equivalents in every scripting language. In a client-server relationship, the server interprets gestures in the order in which they are received, alters the state accordingly, and returns the state.

Any evaluation or operation using data must refer to a value store in the state via an explicit declaration gesture. This makes some things like, like comparing a variable against an inline value (“variableName == ‘a string’”) impossible. Mezzo doesn’t know what to do with unnamed data. The motivation behind this is to make Mezzo compliant with languages that scope variable namespaces differently, and making the program’s state comprehensible and stable at any stage of its interpretation. Say, for instance, that a mezzo iteration gesture stops halfway through getting processed by a python service, and gets passed off to a Ruby or Javascript service. The state knows the current locals being passed to the iterator, and knows which element of the iterable was the last to be successfully passed to the iterator. 


**Declaration**

```json
{ “type”: “declaration” }
```

*Add a namespace to state. Give the namespace a value and type.*
```json
	{ “type” : “primitive”, 
  “nameSpace”: { some object: “variable name”},
               “value”: a primitive }
```

**Alteration**
```json
{ “type”: “alteration” }
```

*Retrieve a namespace from state, alter it, then update state.*

```json
{“left”: { some object: “variable name” },
 “center” : "an alteration operator", 
 “right”: "numeric, defaults to 1" }
```

*Alteration Operators*

- andeq (&=)
- oreq (|=)
- upbit	(>>=)
- downbit	(<<=)
- modeq	(%=) 
- diveq	(^=)
- multeq (*=)
- expeq	(^=)
- pluseq (+=)
- minuseq (-=)

**Iteration**
```json
{ “type”: “iteration” }
```

*Provided an iterable namespace in the state*

```json
	{
“each” : "iterable_namespace",
“local”: “a namespace to store the index or key under”,
“do”:  [ { "type" : "gesture", "body": "..." } ]
}
```

**Recursion**

```json
{ “type”: “recursion” }
```

*Basically for breakable while loop.*

```json
	{ “break”: "a condition gesture",
    “do”: [ { "type" : "gesture", "body": "..." } ] }
```

**Flow**
```json
{ “type”: “flow” }
```

*Only really simple if statements are supported. All flow patterns are chains. The first time an “if” gesture evaluates to true and that “if” object’s “break” attribute is set to True, all subsequent conditions aren’t evaluated. This way we one can produce equivalent “if elsif” flow patterns in various scripting languages.*

```json
{ “chain”: [
{ “if”: comparison gesture,
  “do”: [ { "type" : "gesture", "body": "..." } ],
  “break”: 1 } ] }
```

**Comparison**

```json
{ “type”: “comparison” }
```

*Given **left**, **center** and **right** arguments, evaluates to a Boolean.*

```json
{“chain”: [ { “left”: "state namespace", 
              “center”: “a supported comparison operator”,
              “right”: "state namespace", 
              “negate”: "false" }, 
  		      { “continue": “a relational operator” },
            { “left”: "state namespace", 
              “center”: “a supported comparison operator”,
              “right”: "state namespace", 
              “negate”: "false" } ] }
```

*Supported Comparison Operators*

  * “eq” (==)
  * “ne” (!=)
  * “lt” (<)
  * “gt” (>)
  * “is” (?)

*Relational Operators*

 * “and”	(AND)	
 * “or” (OR)
 * “xor” (XOR)
 * “xand”	(XAND)

**Binding**
```json
{ “type”: “binding” }
```
*Attaches a state namespace to a list of gestures.

	{ “namespace”: { a namespace path },
  “arguments”: { “a named argument” : default value, 
              “a named argument” : default value, 
   … },
              “locals” : [ namespace,
       namespace,
       namespace ] ,
  “gestures” : [ gesture,
           gesture,
           gesture ] }


Invocation

Evaluate a namespaced function with values stored in the state namespace.

	{ “namespace”: { a namespace path } ,
   “arguments”:  { “named argument”: a state namespace,
                “a named argument”: a state namespace }}

Block

Evaluate a set of gestures with a specified open, close and exception arguments. The “except” attribute defaults to “die” but can be set to “recover” in which case the interpreting client recovers from ALL failures in the evaluated “body” gestures.

	{“open”: [ gesture,
   		    gesture, 
                            gesture ], 
	“close”: [ gesture,
   gesture,
   gesture ],
“body”: [ gesture,
  gesture, 
  gesture ]
	“except” : “die / recover” }
