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

function Mezzo (){
    this.state = new MezzoState({});
}

Mezzo.prototype.declarationGesture = function(ns){
    // just declares the given path namespace
    this.state.setNameSpace(ns);
}

function runTests(){
    m = new Mezzo();
    m.state.setNameSpace({'foo': {'baz': 'bar'}});
    console.log(m.state.objects);
}
