// Javascript interpreter for Mezzo scripts
// Deeply unfinished, untested.

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
    if (v){
        var stopAt = nsChain.length - 1;
    } else {
        var stopAt = nsChain.length - 2;
    }
    for (i in nsChain){
        var link = nsChain[i];
        if (i < stopAt){
            if (!referenceDepth.hasOwnProperty(link)){
                // make the refrence depth preceding the literal is an object
                // that accepts literal assignemtn
                referenceDepth[link] = {};
            }
            // lower reference depth
            referenceDepth = referenceDepth[link];
        } else {
            // parse the last two arguments in the chain as a literal
            if (i == (stopAt)){
                if(v){
                    referenceDepth[link] = v;
                } else {
                    referenceDepth[link] = nsChain[nsChain.length-1];
                }
                break;
            }
        }
    }
}

function Mezzo (objects){
    // really trying to discourage any direct interaction
    // with the state object here
    if (typeof objects != 'undefined'){
        this._state = new MezzoState(objects);
    } else {
        this._state = new MezzoState({});
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

Mezzo.prototype.declare = function(obj){
    // just declares the given path namespace
    this.set(obj.namespace);
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
    // TODO
    // {'chain': [{'left': 'a', 'center': 'b', right: 'c'}]}
}

Mezzo.prototype.binding = function(obj){
    // TODO
    // {'namespace': 'a', 'arguments': {}, 'locals': [], 'body': [{}]}
}

Mezzo.prototype.invoke = function(obj){
    // TODO
    // {'namespace': 'a', 'arguments': {}}
}

Mezzo.prototype.flow = function(obj){
    // TODO
    // {'chain': [{if': 'a', 'do': 'b', 'stop': 'c'}]
}

Mezzo.prototype.alter = function(obj){
    // TODO
    // {'left': 'a', 'center': 'b', 'right': 'c'}
}


Mezzo.prototype.deserializeGesture = function(obj){
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


function runTests(){
    m = new Mezzo();
    m.state = {'foo': {'baz': 1}};
    // should show { foo: { baz: 1 } }
    console.log(m._state.objects)
    
    // should show 1
    console.log(m.get({'foo': 'baz'}));
    // should show { foo: { baz: 1 } }
    console.log(m.state);
    
    m = new Mezzo();
    m.declare({'namespace': {'foo': {'baz': 'bar'}}});
    // should show 'bar'
    console.log(m.state.foo.baz);

}

runTests()