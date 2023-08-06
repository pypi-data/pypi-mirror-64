<div class="admonition note">
  <p class="admonition-title">Note</p>
  <p>This is currently an experimental feature. To try it follow this guide.</p>
</div>

## Preparation instructions

### Dependencies

Follow the <a href="../quickstart/#preliminaries">Preliminaries</a> and <a href="../quickstart/#installation">Installation</a> sections from the AEA quick start.

### How to run

First make sure you are inside your AEA's folder (see <a href="../quickstart">here</a> on how to create a new agent).

Then run  

``` bash
aea generate protocol <path-to-protocol-specification>
```

where `<path-to-protocol-specification>` is the relative path to a <a href="../generator/#protocol-specification">protocol specification</a>  file. 


If there are no errors, this command will generate the protocol and place it in your AEA project. The name of the protocol's directory will match the protocol name given in the specification.

## Protocol Specification
A protocol can be described in a yaml file.
As such, it needs to follow the <a href="https://pyyaml.org/wiki/PyYAMLDocumentation" target="_blank">yaml format</a>. 
The following is an example protocol specification:

``` yaml
name: two_party_negotiation
author: fetchai
version: 0.1.0
license: Apache-2.0
description: 'A protocol for negotiation over a fixed set of resources involving two parties.'
speech_acts:
  cfp:
    query: ct:DataModel
  propose:
    query: ct:DataModel
    price: pt:float
  accept: {}
  decline: {}
  match_accept: {}
```


Each protocol specification yaml file contains some basic information about the protocol. The allowed fields and what they represent are:

 * `name`: The name of the protocol (written in <a href="https://en.wikipedia.org/wiki/Snake_case" target="_blank">snake_case</a>)
 * `authors`: List of authors
 * `version`: The current version of the protocol
 * `license`: Licensing information
 * `description`: A short description of the protocol

Each field is a key/value pair, where both the key and the value are yaml strings. Every field is mandatory. 

In addition to the above basic information, a protocol specification must describe the syntax of valid messages according to this protocol.
Therefore, there is another mandatory field: `speech-acts`, which defines the set of performatives valid under this protocol, and a set of contents (i.e. parameters) for each performative.  

The format of the `speech-act` is as follows:
`speech-act` is a dictionary, where each key is a unique **performative** (yaml string), and the value is a **content** dictionary. If a performative does not have any content, then its content dictionary is empty, e.g. `accept`, `decline` and `match_accept` in the above protocol specification.

Each content dictionary is composed of key/value pairs, where each key is the name of a content (yaml string) and the value is its <a href="../generator/#types">type</a> (yaml string). For example, the `query` performative has one content whose name is `query` and whose type is `ct:DataModel`.  

### Types

The specific types which could be assigned to contents in a protocol specification are described in the table below.

Types are either user defined (i.e. custom types) or primitive: 

* Custom types are prepended with `ct:` and their format is described using regular expression in the table below. 
* Primitive types are prepended with `pt:`. There are different categories of primitive types, e.g. &lt;PT&gt; such as integers and booleans, &lt;PCT&gt; such as sets and lists, and so on. Primitive types are compositional: 
    - For example, consider `pt:set` under &lt;PCT&gt;, i.e. an unordered collection of elements without duplicates. A `pt:set` describes the type of its elements (called "sub-type") in square brackets. The sub-type of a `pt:set` could either be a &lt;PT&gt; (e.g. `pt:int`, `pt:bool`) or &lt;CT&gt; (i.e. a custom type). 
    - In describing the format of types, `/` between two sub-types should be treated as "or". For example, the sub-type of a `pt:set` is either a &lt;PT&gt; or a &lt;CT&gt;.

A multi type denotes an "or" separated set of sub-types, e.g. `pt:union[pt:str, pt:int]` as the type of a content `c` means `c` is either a `pt:int` or a `pt:float`.

An optional type for a content denotes that the content's existence is optional, but if it is present, its type must match `pt:optional`'s sub-type. 
                                                                                                                                                                 
| Type                       | Code        | Format                                                                                                      | Example                                | In Python             |
| ---------------------------| ------------| ------------------------------------------------------------------------------------------------------------|----------------------------------------|-----------------------|
| Custom types               | &lt;CT&gt;  | ct:RegExp(^[A-Z][a-zA-Z0-9]*$)                                                                              | ct:DataModel                           | Custom Class          |
| Primitive types            | &lt;PT&gt;  | pt:bytes                                                                                                    | pt:bytes                               | bytes                 |
|                            |             | pt:int                                                                                                      | pt:int                                 | int                   |
|                            |             | pt:float                                                                                                    | pt:float                               | float                 |
|                            |             | pt:bool                                                                                                     | pt:bool                                | bool                  |
|                            |             | pt:str                                                                                                      | pt:str                                 | str                   |
| Primitive collection types | &lt;PCT&gt; | pt:set[&lt;PT&gt;/&lt;CT&gt;]                                                                               | pt:set[ct:DataModel]                   | FrozenSet[DataModel]  |
|                            |             | pt:list[&lt;PT&gt;/&lt;CT&gt;]                                                                              | pt:list[pt:int]                        | Tuple[int, ...]<sup>*</sup>       |
| Primitive mapping types    | &lt;PMT&gt; | pt:dict[&lt;PT&gt;/&lt;CT&gt;, &lt;PT&gt;/&lt;CT&gt;]                                                       | pt:dict[pt:bool, ct:DataModel]         | Dict[bool, DataModel] |
| Multi types                | &lt;MT&gt;  | pt:union[&lt;PT&gt;/&lt;CT&gt;/&lt;PCT&gt;/&lt;PMT&gt;, ..., &lt;PT&gt;/&lt;CT&gt;/&lt;PCT&gt;/&lt;PMT&gt;] | pt:union[pt:str, pt:set[ct:DataModel]] | Union[str, int]       |
| Optional types             | &lt;O&gt;   | pt:optional[&lt;MT&gt;/&lt;PMT&gt;/&lt;PCT&gt;/&lt;PT&gt;/&lt;CT&gt;]                                       | pt:optional[pt:bool]                   | Optional[bool]        |

<sup>*</sup> <sub>This is how variable length tuples containing elements of the same type are declared in Python; see <a href="https://docs.python.org/3/library/typing.html#typing.Tuple" target=_blank>here</a> </sub>

## Demo instructions

First, create a new AEA project:

``` bash
aea create my_aea
cd my_aea
```

Second, run the generator on the sample specification:

``` bash
aea generate protocol ../examples/protocol_specification_ex/sample.yaml
```

This will generate the protocol and place it in your AEA project.

Third, try generating other protocols by first defining a specification, then running the generator.



<br />
