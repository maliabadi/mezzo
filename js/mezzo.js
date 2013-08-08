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
    for (i in nsChain){
        var link = nsChain[i];
        if (i < nsChain.length - 2){
            if (!referenceDepth.hasOwnProperty(link)){
                // make the refrence depth preceding the literal is an object
                // that accepts literal assignemtn
                referenceDepth[link] = {};
            }
            // lower reference depth
            referenceDepth = referenceDepth[link];
        } else {
            // parse the last two arguments in the chain as a literal
            if (i == (nsChain.length - 2)){
                referenceDepth[link] = nsChain[nsChain.length-1];
                break;
            }
        }
    }
}

function Mezzo (objects){
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

Mezzo.prototype.declare = function(ns){
    // just declares the given path namespace
    this._state.setNameSpace(ns);
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
    m.declare({'foo': {'baz': 'bar'}});
    // should show 'bar'
    console.log(m.state.foo.baz);

}

runTests()