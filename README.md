# Mezzo

## Interpreter-Agnostic Script Notation

Mezzo is the least clever programming language possible. It’s a reductive JSON representation of a constrained set of 9 distinct **programming gestures**, as well as a state machine of a program’s current object space. It’s designed to be interpreted, compiled, and operated on asynchronously by client and server-side programs written in Ruby, Python, Javascript, whatever -- Mezzo really doesn't care. By constraining the number of different of different lexical and syntactic concepts available and confining the program to a **state-based, procedural** structure, we eliminate abstract syntax patterns that translate ambiguously in other scripting languages. You could write Mezzo programs and have them interpreted in Python, Ruby or Javascript. Or you could write Python, Ruby or Javascript and have it converted to Mezzo. That's the idae anyway.

### Basics

**Base Template** 
```json
{"state" : {
		"some_name": { "some_attribute" : "value" }
	  },
 "directives" : [ 
  {"type" : "a gesture type",
   "parameters" : {"some": "parameters"}} ]
}
```

**State Namespaces** 

State namespaces are objects and they can be nested. They function
as pathed namespaces, rather than one giant global namespace.


```json
{"an object": {"a nested object": "attribute name"}}
```

**Primitives**

Mezzo support only JSON primitives.

### Gestures

Mezzo is constrained to a very limited vocabulary of programming ideas that have equivalents in every scripting language. In a client-server relationship, the server interprets gestures in the order in which they are received, alters the state accordingly, and returns the state.

Any evaluation or operation using data must refer to a value store in the state via an explicit declaration gesture. This makes some things like, like comparing a variable against an inline value ("variableName == ‘a string’") impossible. Mezzo doesn’t know what to do with unnamed data. The motivation behind this is to make Mezzo compliant with languages that scope variable namespaces differently, and making the program’s state comprehensible and stable at any stage of its interpretation. Say, for instance, that a mezzo iteration gesture stops halfway through getting processed by a python service, and gets passed off to a Ruby or Javascript service. The state knows the current locals being passed to the iterator, and knows which element of the iterable was the last to be successfully passed to the iterator. 


**Declaration**

```json
{ "type": "declaration" }
```

*Add a namespace to state. Give the namespace a value and type.*
```json
	{ "type" : "primitive",
      "namespace": { "some object": "attribute name"},
                     "value": 1 }
```

**Alteration**
```json
{ "type": "alteration" }
```

*Retrieve a namespace from state, alter it, then update state.*

```json
{"left" : { "some object": "attribute name"},
 "center" : "andeq", 
 "right" : 1 }
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
{ "type": "iteration" }
```

*Provided an iterable namespace in the state*

```json
	{ "each" : {"an object": {"a nested object": "attribute name for an iterable feature"}},
	  "local" : {"iterable locals": "attribute name for an iterable feature"},
      "do" : [ { "type" : "gesture", "body" : "..." } ]
}
```

**Recursion**

```json
{ "type": "recursion" }
```

*Basically for breakable while loop.*

```json
	{ "break": { "type": "comparison", "chain" : [] },
      "do": [ { "type" : "gesture", "body": "..." } ] }
```

**Flow**
```json
{ "type": "flow" }
```

*Only really simple if statements are supported. All flow patterns are chains. The first time an "if" gesture evaluates to true and that "if" object’s "break" attribute is set to True, all subsequent conditions aren’t evaluated. This way we one can produce equivalent "if elsif" flow patterns in various scripting languages.*

```json
{ "chain": [
{ "if": { "type": "comparison", "chain" : []},
  "do": [ { "type" : "gesture", "body" : "..." } ],
  "break": 1 } ] }
```

**Comparison**

```json
{ "type": "comparison" }
```

*Given "left", "center" and "right" arguments, evaluates to a Boolean. Comparisons*

```json
{ "chain": [ { "left": {"an object": {"a nested object": "attribute name"}}, 
               "center": "eq",
               "right": {"an object": {"a nested object": "attribute name"}}, 
               "negate": "false" },
             { "continue": "and" },
            { "left": {"an object": {"a nested object": "attribute name"}}, 
              "center": "lt",
              "right": {"an object": {"a nested object": "attribute name"}}, 
              "negate": "false" } ] }
```

Comparison Operators

  * "eq" (==)
  * "ne" (!=)
  * "lt" (<)
  * "gt" (>)
  * "is" (?)

Relational Operators

 * "and" (AND)	
 * "or" (OR)
 * "xor" (XOR)
 * "xand" (XAND)

**Binding**
```json
{ "type" : "binding" }
```
*Attaches a state namespace to a list of gestures that may or may not operate on any locals declared in the body of the directives*

```json

	{ "namespace": {"an object": {"a nested object": "attribute name"}},
      "arguments": { "a named argument" : "default value", 
      		         "a named argument" : "default value" },
      "locals" : [ "attribute name", "attibute name", "attribute name"],
      "directives" : [ { "type" : "gesture", "body": "..." } ] }
```
**Invocation**
```json
{ "type" : "invocation" }
```
*Evaluate a namespaced function with values stored in the state with a preceding Declaration gesture.*

```json
	{ "namespace": {"an object": {"a nested object": "attribute name"}},
      "arguments": { "named argument" : { "some": "namespace path" },
                     "a named argument": { "some": "namespace path" }}}
```

**Block**

*A very limited interpretation of the functionality of blocks of code. Evaluates a set of gestures with specified open, close and exception gesture lists. The "except" attribute defaults to "die" but can be set to "recover" in which case the interpreting client recovers from ALL failures in the evaluated "body" gestures.*

```json
	{"open": [ { "type" : "gesture", "body": "..." } ],
	"close": [ { "type" : "gesture", "body": "..." } ],
	"body": [ { "type" : "gesture", "body": "..." } ],
	"except" : "die" }
```
