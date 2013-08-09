// Javascript interpreter for Mezzo scripts

// BEGIN MezzoState 

function MezzoState(obj){
    this.supportedTypes = ["Array",
                           "String",
                           "Boolean",
                           "Number"];
    this.objects = {};
    for (attribute in obj){
        this.objects[attribute] = obj[attribute];
    }
}

MezzoState.prototype.generatePathChain = function(ns){
    // takes a nested set of objects that reference
    // a state namespace and spits out dot notation
    // e.g. {'foo': {'baz': 'bar'}} becomes ['foo', 'baz', 'bar']
    var chain = [];
    var nsdup = ns;
    while (nsdup.constructor.name == "Object"){
        for (attr in nsdup){
            if (this.supportedTypes.indexOf(nsdup[attr].constructor.name) > -1){
                // push both the key and the value onto the chain
                chain.push(attr)
                chain.push(nsdup[attr]);
                // stop recursion
                nsdup = false;
                // break the loop
                break;
            } else {
                // push the attribute name onto the chain
                chain.push(attr);
                // lower the reference depth
                nsdup = nsdup[attr];
            }
        }
    }
    return chain;
}

MezzoState.prototype.getNameSpace = function(ns){
    var nsChain = this.generatePathChain(ns);
    var referenceDepth = this.objects;
    for (i in nsChain){
        var link = nsChain[i];
        if (!referenceDepth.hasOwnProperty(link)){
            referenceDepth[link] = {};
        }
        referenceDepth = referenceDepth[link];
    }
    return referenceDepth;
}

MezzoState.prototype.setNameSpace = function(ns, v){
    var nsChain = this.generatePathChain(ns);
    var referenceDepth = this.objects;
    var stopAt = nsChain.length - 1;
    if (!v) { stopAt -= 1; }
    for (i in nsChain){
        var link = nsChain[i];
        if (i < stopAt){
            if (!referenceDepth.hasOwnProperty(link)){
                // make sure the reference depth preceding the literal is an object
                // that accepts literal assignemtn
                referenceDepth[link] = {};
            }
            // lower reference depth
            referenceDepth = referenceDepth[link];
        } else {
            // parse the last two arguments in the chain as a literal
            if (i == (stopAt)){
                var right = v;
                if (!right){ right = nsChain[nsChain.length-1] }
                referenceDepth[link] = right;
                break;
            }
        }
    }
}

// END MezzoState

// BEGIN Mezzo Core

function Mezzo (objects){
    // really trying to discourage any direct interaction
    // with the state object here
    if ( typeof(objects != 'undefined')
         && objects.constructor.name == "Object" ){
        if ( objects.hasOwnProperty('objects') ){
            this._state = new MezzoState(objects.objects);
        } else {
            this._state = new MezzoState({});
        }
        if ( objects.hasOwnProperty('directives') ) {
            this.directives = objects.directives;
        } else {
            this.directives = [];
        }
    } else {
        this._state = new MezzoState({});
        this.directives = [];
    }

    this.__defineGetter__("state", function(){
        return this._state.objects;
    });
    this.__defineSetter__("state", function(obj){
        if ( obj.constructor.name == "MezzoState" ) {
            this._state = obj;
        } else if (obj.constructor.name == "Object") {
            this._state = new MezzoState(obj);
        }
    });
    this.get = function(ns){
        return this._state.getNameSpace(ns);
    }
    this.set = function(ns){
        this._state.setNameSpace(ns);
    }
}

Mezzo.prototype.run = function(){
    for ( i in this.directives ){
        this.deserializeGesture(this.directives[i]);
    }
}

Mezzo.deserialize = function(json){
    return new Mezzo ( JSON.parse(json) );
}

Mezzo.prototype.declare = function(obj){
    // just declares the given path namespace
    this.set(obj.namespace);
}

Mezzo.prototype.alter = function(obj){
    // e.g. {'left': 'a', 'center': 'b', 'right': 'c'}
    var left = this.get(obj.left);
    var right = this.get(obj.right);
    var alteredValue;
    switch(obj.center){
        case "andeq":
            alteredValue = left && right;
            break;
        case "andeq":
            alteredValue = left || right;
            break;
        case "upbit":
            alteredValue = left >> right;
            break;
        case "downbit":
            alteredValue = left >> right;
            break;
        case "modeq":
            alteredValue = left % right;
            break;
        case "diveq":
            alteredValue = left / right;
            break;
        case "multeq":
            alteredValue = left * right;
            break;
        case "expeq":
            alteredValue = Math.pow(left, right);
            break;
        case "pluseq":
            alteredValue = left + right;
            break;
        case "minuseq":
            alteredValue = left - right;
            break;
    }
    this._state.setNameSpace(obj.left, alteredValue);
}

Mezzo.prototype.each = function(obj){
    // the 'each' attribute is a namespace
    // that refers to an array object in the instance state
    each = this.get(obj.each)
    for (k in each){
        // the 'local' attribute is a namespace that we load
        // the object we're current iterating over into
        this.set(obj.local, each[i]);
        for (i in obj.gestures) {
            gest = obj.gestures[i];
            // deserialize and run gesture
            this.deserializeGesture(gest)
            // increment interation index
        }
    }
}

Mezzo.prototype.compare = function(obj){
    // e.g. {'chain': [{'left': 'a', 'center': 'b', right: 'c'}]}
    var evalchain = [];
    var breakonfalse = false;
    var procede = true;
    var lasteval = function(){
        if(!evalchain.length){
            return true;
        } else {
            return evalchain[evalchain.length - 1];
        }
    }
    while ( procede ){
        for (i in obj.chain){
            co = obj.chain[i];
            if ( co.hasOwnProperty('continue') ){
                // handle relational operators
                // the appear between comparisons
                if ( co.continue == 'and' ){
                    // if the left operand is false
                    // break and stop recursion immediately
                    if (!lasteval()){
                        procede = false;
                        break;
                    } else {
                        // prepare to break if upcoming
                        // right operand is false
                        breakonfalse = true;
                    }
                }
                if ( co.continue == 'or' ){
                    if (lasteval()){
                        // if the left argument evaluated
                        // as true, don't be ready to break
                        // if the next statement comes out false
                        breakonfalse = false;
                    } else {
                        // if the last statement was false
                        // break if the next statement is false
                        breakonfalse = true;
                    }
                    continue;
                }
                if ( co.continue == 'xand'){
                    // not both
                    if (!lasteval()) {
                        // pass if the last statement evaluated
                        // to false, and don't break if the next
                        // statement evaluates to false
                        breakonefalse = false;
                    } else {
                        // if the first statement evaluated to true
                        // the xand criteria is categorically broken
                        // break recursion
                        procede = false;
                        // break loop
                        break;
                    }
                    continue;
                }
                if (co.continue == 'xor'){
                    // one of the two operands is true
                    // but not both of them
                    if (!lasteval()) {
                        breakonfalse = false;
                    } else {
                        breakonfalse = true;
                    }
                    continue;
                }
            } else {
                // rather than the namespace refrence
                // the actual data those namespaces refer to
                var left = this.get(co.left);
                var right = this.get(co.right);
                // a bit of ugliness that is unavoidable
                // until someone tells me a way to invoke
                // Javascript comparison operators by name
                switch(co.center){
                    case "eq":
                        var evaluation = left == right;
                        break;
                    case 'ne':
                        var evaluation = left != right;
                        break;
                    case 'lt':
                        var evaluation = left < right;
                        break;
                    case 'gt':
                        var evaluation = left > right;
                        break;
                    case 'is':
                        var evaluation = right && left;
                        break;
                }
                if (breakonfalse && !lasteval()){
                    // if the breakonfalse state is set to true
                    // and the last comparison evaluated to false
                    // then stop recursion
                    procede = false;
                    // and break the loop
                    break;
                }
            }
        }
        // if every comparison in the chain has completed without
        // breaking, stop recursion
        procede = false;
    }
    return lasteval();
}

Mezzo.prototype.flow = function(obj){
    if ( obj.constructor.name != "Object" || !obj.hasOwnProperty('chain')) {
        throw "Invalid argument passed to Mezzo.flow function";
    }
    // iterate over chain
    for (i in obj.chain){
        // each link in the chain looks like this:
        // {'comparison': {'chain': [{'left': 'a', 'center': 'b', 'right': 'c'}]}
        //  'do': [{'type': 'somegesture': {'foo': 'bar'}}]}
        //  'stop': true}
        var link = obj.chain[i];
        if (!link.constructor.name == "Object"){
            throw "Misconstructed Flow Element";
        }
        // check the link for required properties
        var required = ['comparison', 'do', 'stop'];
        for (r in required){
            if(!link.hasOwnProperty(required[r])) throw "Misconstructed Flow Element";
        }
        // if the evaluation gesture evaluates to true
        if ( this.compare(link.comparison) == true ){
            for (k in link.do){
                this.deserializeGesture(link.do[k]);
            }
        }
        if ( link.stop ) {
            break;
        }
    }
}

Mezzo.prototype.binding = function(obj){
    // TODO
    // {'namespace': 'a', 'arguments': {}, 'locals': [], 'body': [{}]}
    var chain = this._state.generatePathChain(obj.namespace);
    var referenceDepth = this.state;
    for ( i in chain ){
        var link = chain[i];
        if (!referenceDepth.hasOwnProperty(link) ||
            !referenceDepth[link].constructor.name == "Object"){
            referenceDepth[link] = {'body': obj.body, 'arguments': obj.arguments, 'locals': obj.locals};
        }
        referenceDepth = referenceDepth[link];
    }
}

Mezzo.prototype.invoke = function(obj){
    required = ['namespace', 'arguments']
    for ( r in required ) {
        if ( !obj.hasOwnProperty(required[r])) throw "Misconstructed Invocation";
    }
    // {'namespace': 'a', 'arguments': {}}
    var func = this.get(obj.namespace);
    // func[arguments] = obj.arguments
    var chain = this._state.generatePathChain(obj.namespace);
    var referenceDepth = this.state;
    for ( i in chain ){
        var link = chain[i];
        if (i >= chain.length - 1){
            // wait until the last reference in the chain
            // and reset the function' attributes 
            func.arguments = obj.arguments;
            referenceDepth[link] = func;
            break;
        }
        referenceDepth = referenceDepth[link];
    }

    for ( i in func.body ) {
        this.deserializeGesture(func.body[i]);
    }

}


Mezzo.prototype.deserializeGesture = function(obj){
    supported = ['declaration', 'iteration', 'comparison', 
                 'invocation', 'flow', 'binding', 'alteration'];
    if (!obj.constructor.name == "Object"){
        throw "Invalid argument passed to Mezzo.deserializeGesture function";
    }
    if ( supported.indexOf(obj.type) == -1) {
        throw "Unsupported Gesture Type"
    }
    switch(obj.type)
    {
        case 'declaration':
            this.declare(obj);
        case 'iteration':
            this.each(obj);
        case 'comparison':
            this.compare(obj);
        case 'invocation':
            this.invoke(obj);
        case 'flow':
            this.flow(obj);
        case 'binding':
            this.binding(obj);
        case 'alteration':
            this.alter(obj);
    }
}


// BEGIN TESTS

function testSetState(){
    m = new Mezzo();
    m.state = {'foo': {'baz': 1}};
    // should show { foo: { baz: 1 } }
    console.log(m._state.objects)
}

function testSet(){
    m = new Mezzo({'foo' : 'baz'});
    m.set({'foo': {'baz': 1}});
    // should show { foo: { baz: 1 } }
    console.log(m.state);
}

function testGet(){
    m = new Mezzo();
    m.state = {'foo': {'baz': 1}};
    // should show 1
    console.log(m.get({'foo': 'baz'}));
}

function testDeclare(){
    m = new Mezzo();
    m.declare({'namespace': {'foo': {'baz': 'bar'}}});
    console.log(m.state.foo.baz);
}

function testAlter(){
    var m = new Mezzo({'objects': {'foo': {'a': 0, 'b': 1, 'c': 2, 'd': 0}}});
    m.alter({'left': {'foo': 'c'}, 'center': 'pluseq', 'right': {'foo' : 'b'}});
    console.log(m.state);
    // { foo: { a: 0, b: 1, c: 3, d: 0 } }

}

function testCompare(){
    var m = new Mezzo({'objects': {'foo': {'a': 0, 'b': 1, 'c': 2, 'd': 0}}});
    var chain = [{"left": {"foo": "a"},
                  "center": "eq",
                  "right": {"foo": "d"}},
                 {"continue": "and"},
                 {"left": {'foo': 'c'},
                  "center": "gt",
                  "right": {'foo': 'b'}}];
    // should show 'true'
    console.log(m.compare({'chain': chain}));
}

function testFlow(){
    var flow = {'chain': [{'comparison': {'chain' : [{"left": {"foo": "a"}, "center": "eq", "right": {"foo": "d"}}]},
                           'do': [{'type': 'alteration', 'left': {'foo': 'c'}, 'center': 'pluseq', 'right': {'foo' : 'b'}}],
                           'stop': false }]};
    var m = new Mezzo({'objects': {'foo': {'a': 0, 'b': 1, 'c': 2, 'd': 0}}});
    m.flow(flow);
    // { foo: { a: 0, b: 1, c: 3, d: 0 } }
    console.log(m.state)
}


function testBinding(){
    var bound = {'namespace': {'foo': 'myfunction'}, 
                 'arguments': {'argone': 1, 'argtwo': 2},
                 'locals': ['localone', 'localtwo'],
                 'body': [{'type': 'alteration',
                          'left': {'foo': {'baz': 'bar'}},
                          'center': 'pluseq',
                          "right": {'foo': 'adder'}}]};
    var m = new Mezzo({'objects': {'foo': {'varone': 0, 'adder': 1}}});
    m.binding(bound);

    // should show ['localone', 'localtwo']
    console.log(m.state.foo.myfunction.locals)
    // should show {'argone': 1, 'argtwo': 2}
    console.log(m.state.foo.myfunction.arguments)
    // should show [{'type': 'alteration',
    //               'left': {'foo': {'baz': 'bar'}},
    //               'center': 'pluseq',
    //               "right": {'foo': 'adder'}}]
    console.log(m.state.foo.myfunction.body)
}

function testInvocation(){
    var bound = {'namespace': {'foo': 'myfunction'}, 
                 'arguments': {'argone': 1, 'argtwo': 2},
                 'locals': ['localone', 'localtwo'],
                 'body': [{'type': 'alteration',
                           'left': {'foo': 'varone'},
                           'center': 'pluseq',
                           "right": {'foo': 'adder'}}]};
    var m = new Mezzo({'objects': {'foo': {'varone': 0, 'adder': 1}}});
    m.binding(bound);
    // should show 0
    console.log(m.state.foo.varone);
    m.invoke({'namespace': {'foo' : 'myfunction'}, 'arguments': {'argone': 3, 'argtwo': 4}});
    // should show 1
    console.log(m.state.foo.varone);
}