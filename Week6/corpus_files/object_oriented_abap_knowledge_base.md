# Introduction to Object-Oriented Programming

## The Need for a Better Abstraction

### The Evolution of Programming Languages
Programming languages evolved from low-level assembly languages toward higher-level procedural languages such as C and ABAP to improve the expressiveness and quality of abstraction. Assembly language required direct manipulation of central processing unit registers and binary data. Higher-level procedural languages introduced intuitive data types, named variables, structured control statements, and callable procedures. 

Despite these developments, procedural programming requires solutions to be structured around computer architecture rather than the problem domain. This discrepancy between the problem space and the software solution space is termed semantic dissonance. When software models do not directly mirror the business requirements, translation errors occur and system maintenance overhead increases.

### Moving Towards Objects
Object-oriented programming bridges the divide between the problem domain and the software solution space. Instead of translating real-world requirements into separate collections of global data structures and procedural routines, object-oriented design models software as autonomous entities called objects. 

Modeling systems after problem-space concepts eliminates the requirement for intermediate conceptual translations. Autonomous objects encapsulate distinct responsibilities, which improves system comprehension, simplifies maintenance, and promotes modular code reuse across business applications.

## Classes and Objects

### Object Concepts and Definitions
An object is an autonomous runtime instance that encapsulates both state and behavior within a self-contained unit. The state of an object is represented by its attributes, which store instance-specific data. The behavior of an object is defined by its methods, which execute operations on that data. 

Objects represent problem-space entities rather than computer hardware constructs. Encapsulating data and operations together allows an object to act independently according to predefined rules, maintaining its internal consistency across runtime operations.

### Class Concepts and Type Definitions
A class is a formal definition and blueprint from which runtime object instances are created. A class acts as a specialized abstract data type that specifies the attributes, methods, and events that instances of that class possess. 

In ABAP, declaring a class definition defines a custom object type in the same manner that a structured type definition defines the layout of a data structure. When an object is instantiated at runtime based on a class, memory is allocated specifically for that instance. Multiple instances of the same class maintain independent attribute values in separate memory locations, sharing only the structural specification and logic defined by the class.

### Class Interfaces
The interface of a class consists of the operations through which external consumers interact with object instances at runtime. Methods form the primary components of this interface, serving as callable interaction points analogous to procedural function modules or subroutines. 

Through its interface, a class exposes available actions while keeping internal data manipulation in context. Because an object contains both its state and its operational logic, the object executes requested operations autonomously without requiring external programs to manage the internal state variables.

## Establishing Boundaries

### Encapsulation and Implementation Hiding
Encapsulation is the design principle of enclosing data and related operations within a single entity while restricting external access to internal implementation details. The external interface is kept minimal and focused on essential business operations.

Implementation hiding insulates volatile, complex, or security-sensitive components from external consumers. Separating the stable public interface from the internal implementation establishes loose coupling between collaborating components. Internal logic, data structures, or database access routines can be refactored or optimized without invalidating or requiring changes to the programs that consume the class.

### Visibility Sections
Object-oriented programming languages enforce architectural boundaries by dividing class component declarations into distinct visibility sections. The ABAP runtime environment strictly enforces access permissions across three visibility levels:
- Public Section: Components declared in the public section form the general external interface of the class. These attributes, methods, and events are accessible by any consumer program or object that has visibility to the class itself.
- Protected Section: Components declared in the protected section are accessible only by the defining class and its subclasses within an inheritance hierarchy. Protected components remain invisible and inaccessible to general external consumers.
- Private Section: Components declared in the private section are completely hidden from external consumers and subclasses. Private components can only be referenced by methods implemented directly within the defining class.

## Object Reuse

### Composition
Composition is a reuse technique in which complex objects are assembled using existing objects as internal attributes. A containing class incorporates an object reference to another class as a member variable, delegating specific responsibilities to that referenced instance. 

Composition represents a "has-a" relationship between entities. Member objects can be hidden within the private visibility section, allowing the containing class to modify how member instances are created, configured, and utilized without affecting external consumers.

### Inheritance
Inheritance is a code reuse mechanism that establishes a hierarchical generalization and specialization relationship between classes. A specialized class, designated as a subclass, is derived from a generalized class, designated as a superclass. 

The subclass inherits all attributes, methods, and types declared in the superclass. A subclass can introduce new components to support specialized requirements or modify inherited behavior. Changes applied to a superclass automatically propagate down the inheritance hierarchy to all derived subclasses. Inheritance represents an "is-a" relationship, meaning the subclass shares the type of the superclass and can be addressed using the same external interface.

### Polymorphism
Polymorphism denotes the capability of different classes within an inheritance hierarchy to respond to identical method calls in specialized ways. Subclasses inherit the method signatures defined in their superclass but can redefine the underlying implementation logic to meet type-specific requirements.

Because subclasses share the public interface of the superclass, calling programs can interact with specialized subclass instances using a generic superclass reference. The runtime environment evaluates the dynamic type of the object instance at runtime and dispatches execution to the appropriate subclass implementation. Polymorphic method invocation enables generic processing routines to manipulate collections of related objects without containing conditional branching logic for individual object types.

## Object Management
Object management encompasses the lifecycle of an object, from allocation and initialization to deallocation. In ABAP Objects, the runtime environment does not create objects automatically upon variable declaration; object instances must be explicitly instantiated by the program.

Object initialization is handled by specialized methods termed constructors. When memory is allocated for an object instance, the runtime environment automatically invokes the instance constructor before returning the object reference to the caller. The constructor establishes a valid and consistent initial state for the object.

## Unified Modeling Language Class Diagram Basics

### Class Diagrams
Class diagrams are static structural diagrams in the Unified Modeling Language (UML) that depict the static architecture of an object-oriented system. A class diagram illustrates the classes comprising the system, their internal components, and the structural relationships connecting them.

### Class Representation
In UML class diagrams, a class is represented by a rectangular box divided into three horizontal compartments:
- Top Compartment: Contains the name of the class along with optional modifiers such as stereotypes or abstract indicators.
- Middle Compartment: Contains prominent attributes declared by the class.
- Bottom Compartment: Contains relevant operations or methods provided by the class.

### Attribute Specification
Attributes in a UML class diagram are documented using a standardized notation consisting of visibility, name, type expression, initial value, and property strings.
- Visibility: Indicated by a prefix symbol, where `+` designates public visibility, `-` designates private visibility, and `#` designates protected visibility.
- Name: Specifies the identifier of the attribute.
- Type Expression: Identifies the data type, collection structure, or cardinality of the attribute.
- Initial Value: Specifies an optional default value assigned to the attribute.
- Property String: Optional bracketed annotations, such as `{readOnly}`, that document additional design constraints.

### Operation Specification
Operations in a UML class diagram are documented using visibility, name, parameter lists, return types, and property strings.
- Visibility: Represented by `+` for public, `-` for private, and `#` for protected access.
- Parameter List: A comma-separated list enclosed in parentheses. Each parameter specifies a direction kind (`in` for pass-by-value input, `out` for pass-by-value output, `inout` for pass-by-reference), a parameter name, a data type, and an optional default value.
- Return Type: Specifies the data type returned by a functional operation.
- Property String: Optional bracketed tags, such as `{query}`, denoting operations that execute without modifying object state.

### Association Specification
An association represents a structural relationship between classes, depicted as a line connecting two class rectangles. A directed association uses an arrow to indicate navigability from a source class to a target class, signifying that the source class maintains an attribute referencing the target class. A bidirectional association lacks directional arrows or contains arrows at both ends, indicating mutual navigability.

Cardinality notations placed at the association ends define the allowed number of related instances:
- `0..1`: Zero or one instance.
- `1`: Exactly one instance.
- `*`: Zero or more instances.
- `m..n`: A specified numeric range with lower and upper bounds.

### Diagram Notes
Notes in UML diagrams provide explanatory comments or requirements that cannot be captured using standard graphical symbols. A note is depicted as a rectangle with a folded top-right corner and is attached to specific diagram elements via a dashed line.

---

# Getting Started with Objects

## Defining Classes

### Class Declaration Syntax and Naming Conventions
In ABAP Objects, local classes are declared within a `CLASS ... DEFINITION ... ENDCLASS` block. A class definition comprises a declaration section and an implementation section wrapped by `CLASS ... IMPLEMENTATION ... ENDCLASS`. 

The declaration section contains the component declarations organized under `PUBLIC SECTION`, `PROTECTED SECTION`, and `PRIVATE SECTION` statements. Each visibility section is optional, but declared sections must appear in this specific sequence.

Class names in the ABAP Repository and local programs adhere to a 30-character limit. Standard naming conventions use specific prefixes:
- `LCL_`: Local class defined within an ABAP program or include.
- `ZCL_` or `YCL_`: Customer-defined global repository class.
- `CL_`: SAP standard global repository class.
- `/<namespace>/CL_`: Partner- or vendor-defined global class within a registered development namespace.

### Component Declarations
Class components are categorized by scoping level:
- Instance Components: Exist separately for each object instance. Each instance maintains its own memory space for instance attributes. Instance methods evaluate and alter the instance-specific state.
- Class Components (Static Components): Exist once per class, independent of object instances. Class components are declared once and shared across all instances of the class within an internal session.

All component identifiers within a class share a single internal namespace. An attribute, a method, an event, or a type cannot share an identical name within the same class, even if they reside in different visibility sections.

Attributes are internal data objects declared within the class:
- Instance attributes are declared using the `DATA` statement.
- Class attributes (static attributes) are declared using the `CLASS-DATA` statement.
- Constants are declared using the `CONSTANTS` statement and function as read-only static attributes.

Standard naming conventions prefix instance attributes with `m` followed by the type identifier (`v` for elementary value, `s` for structure, `t` for internal table, `o` for object reference). Static attributes use prefix `s`, and constants use prefix `CO_`.

Methods represent procedural routines declared using `METHODS` for instance methods or `CLASS-METHODS` for class methods. A method declaration signature includes:
- `IMPORTING`: Defines input parameters passed into the method. By default, importing parameters are passed by reference and are write-protected inside the method.
- `EXPORTING`: Defines output parameters returned to the caller.
- `CHANGING`: Defines input and output parameters that can be passed in and updated.
- `RETURNING`: Defines a single return value for a functional method.
- `VALUE`: Specifies pass-by-value semantics. When omitted, parameters are passed by reference.
- `OPTIONAL`: Marks a formal parameter as non-mandatory.
- `DEFAULT`: Provides a default value for an optional input parameter.
- `EXCEPTIONS`: Declares non-class-based exception codes.
- `RAISING`: Declares class-based exception classes propagated by the method.

Events model state occurrences that trigger notifications to registered listeners. Instance events are declared using `EVENTS`, while class events are declared using `CLASS-EVENTS`. Event declarations only support `EXPORTING` parameters, and all event parameters must be passed by value via `VALUE(...)`. The ABAP runtime environment implicitly provides a parameter named `sender` containing a reference to the raising instance.

Types within a class are declared using the `TYPES` statement. Class-defined types are static and available across the class. External type groups from the ABAP Dictionary are made available within local class definitions using the `TYPE-POOLS` statement.

### Implementing Methods
Methods declared in the `CLASS ... DEFINITION` section must be implemented in the corresponding `CLASS ... IMPLEMENTATION` block using `METHOD ... ENDMETHOD` processing blocks. Method signatures are not restated in the implementation block.

ABAP Objects enforces strict syntax rules that invalidate obsolete procedural language constructs. Within methods, procedural constructs such as declarative header lines on internal tables, obsolete calculation statements, and untyped parameters produce compilation syntax errors.

Variable scoping within a method resolves identifiers in the following order:
1. Method-local variables declared within the `METHOD ... ENDMETHOD` block.
2. Instance attributes of the class.
3. Class attributes of the class.
4. Global variables of the master program.

Defining a local variable with the same name as an instance or class attribute shadows the class attribute within the method scope.

## Working with Objects

### Object References
ABAP programs access runtime objects indirectly via object reference variables. An object reference variable stores the memory address of an object rather than the object data itself. Object reference variables are declared using the `TYPE REF TO <class_name>` addition with the `DATA` statement.

### Creating Objects
Object instances are instantiated dynamically at runtime using the `CREATE OBJECT` statement. When executed, the runtime environment:
1. Determines memory requirements from the referenced class definition.
2. Allocates heap memory in the extended memory area.
3. Allocates an object header containing administrative metadata.
4. Executes the instance constructor method if one is defined.
5. Writes the memory address of the object header into the target object reference variable.

### Object Reference Assignments
Object reference variables are assigned using the assignment operator (`=`). Assigning one reference variable to another copies the memory address, not the underlying object instance. Multiple reference variables can point simultaneously to the same object instance. Modifications executed through one reference variable immediately affect the object referenced by all other pointing variables.

When all reference variables pointing to an object instance are cleared or overwritten, the object becomes unreferenced (orphaned) and eligible for memory reclamation by the garbage collector.

### Accessing Instance Components
Instance attributes and instance methods are accessed externally using the object component selector operator (`->`). Methods can be invoked using the direct call syntax `oref->method( ... )` or the statement `CALL METHOD oref->method( ... )`.

Within instance methods, the current object instance is addressed using the predefined self-reference variable `me`. The `me` reference is implicitly defined for every instance and points to the executing instance itself. `me` can be used to qualify shadowed instance attributes or to pass the current instance as a parameter to other methods.

### Accessing Class Components
Class components (static attributes, constants, and static methods) are accessed without an object reference using the class component selector operator (`=>`). The syntax follows the format `<class_name>=><component_name>`. Within the defining class, the class name prefix is optional because the static context is implicitly known.

### Working with Events
ABAP Objects provides an event mechanism based on the publish-subscribe design pattern:
- Raising Events: An object triggers an event using the `RAISE EVENT <event_name> EXPORTING ...` statement.
- Event Handler Methods: Methods designed to capture events are declared using the `METHODS <method_name> FOR EVENT <event_name> OF <class_name>` statement. The parameter list of the event handler method must match the exporting parameters of the event.
- Registering Handlers: Event handler methods are registered at runtime using the `SET HANDLER` statement. For instance events, the registration can specify a single instance using `FOR oref` or all instances using `FOR ALL INSTANCES`. Class events do not accept instance qualifiers. Event handling can be toggled dynamically using the `ACTIVATION` addition passing `'X'` to activate or space to deactivate.

### Working with Functional Methods
A functional method is a method that defines a single `RETURNING` parameter and any number of `IMPORTING` parameters. Functional methods can be used directly in operand positions across ABAP statements, including:
- Logical expressions in `IF`, `ELSEIF`, and `WHILE` statements.
- Case selectors in `CASE` statements.
- `WHERE` conditions in `LOOP AT`, `DELETE`, and `MODIFY` internal table operations.

In Release 7.40 and higher, functional methods support `EXPORTING` and `CHANGING` parameters alongside the `RETURNING` parameter. Release 7.40 also introduced predicative method calls, allowing a functional method call to serve as a standalone relational expression in logical statements without an explicit comparison operator. If the functional method returns an initial value, the predicate evaluates to false; any non-initial return value evaluates to true.

### Chaining Method Calls
Method call chaining enables multiple method invocations within a single statement using consecutive object component selector operators (`->`). Method chaining requires each intermediate method in the chain to be a functional method that returns an object reference. Returning the self-reference `me` enables fluent method chaining on the same object instance.

## Creating an Executable Program with Local Classes

### Report Program Creation
Local classes can be developed inside executable report programs using the Object Navigator (Transaction `SE80`). When creating a program, the program name and title are defined, and the program is assigned to a development package such as `$TMP` for local, non-transportable objects.

### Incorporating Local Class Definitions
A local class definition and its implementation can be placed directly in the main report source code or organized into separate include programs. To structure execution according to object-oriented principles, procedural report events such as `START-OF-SELECTION` are restricted to instantiating the class or invoking a static entry method such as `main`, delegating all business logic to object-oriented class components.

## Working with Global Classes

### The Class Pool Concept
Global classes are standalone repository artifacts stored in program containers called class pools. A class pool has program type `K` and cannot be executed directly via transaction codes or submit statements. A class pool contains the definition and implementation of a single global class, along with local definitions, types, and test classes required to support the global class.

### Accessing the Class Builder
Global classes are created and maintained using the Class Builder, accessible via Transaction `SE24` or within the Object Navigator (Transaction `SE80`) by selecting the Class / Interface category.

### Global Class Creation
When creating a global class in the Class Builder, the following properties are configured:
- Class Name: Must adhere to naming standards (`ZCL_`, `YCL_`, or namespace prefixes).
- Description: Short text describing the class purpose.
- Instantiation Generation: Specifies whether instantiation is `Public`, `Protected`, `Private`, or `Abstract`.
- Class Type: Options include `Usual ABAP Class`, `Exception Class`, `Persistent Class`, and `Test Class (ABAP Unit)`.
- Final Checkbox: When selected, declares the class as `FINAL`, preventing inheritance.

### Component Definition in the Form-Based Editor
The form-based editor of the Class Builder organizes component definitions across dedicated tabs:
- Attributes Tab: Defines attributes by specifying attribute name, level (Instance Attribute, Static Attribute, Constant), visibility (Public, Protected, Private), read-only flag, typing method, associated data type, and initial value. The Direct Type Entry option allows editing type definitions in code.
- Methods Tab: Declares methods by specifying method identifier, level (Instance Method, Static Method), visibility, and description. Selecting a method and choosing the Parameters button displays parameter definitions. Method implementations are coded by double-clicking the method or selecting the Source Code button.
- Events Tab: Declares events by specifying event identifier, level (Instance Event, Static Event), and visibility. Selecting the Parameters button displays event export parameters.
- Types Tab: Defines class-level types using the form or Direct Type Entry.
- Local Definitions / Implementations Button: Opens an editor section containing local macros, data types, and local helper classes available only within the class pool.

### The Source Code-Based Editor
In SAP NetWeaver 7.02 and higher, the Class Builder provides a Source Code-Based mode that displays the entire class pool as a continuous text file. Developers can switch between the form-based editor and the source code editor using the corresponding toolbar toggle buttons.

## Developing Classes Using ABAP Development Tools in Eclipse

### Architecture of ABAP Development Tools
ABAP Development Tools (ADT) in Eclipse provides an Eclipse-based development environment that connects to the AS ABAP backend via REST-based web services. Source code and repository metadata remain stored on the AS ABAP application server database; the local Eclipse workspace maintains only project connection parameters and IDE configuration files.

### Configuration and Project Setup
Connecting Eclipse to an AS ABAP system requires the backend to be running SAP Kernel 7.20 or higher and SAP BASIS 7.31 Support Package Stack 04 or higher. An ABAP Project is created in Eclipse by selecting an existing SAP Logon connection, authenticating with system credentials, and selecting favorite development packages. The ABAP perspective configures the layout with the Project Explorer, Outline view, editor area, and diagnostic views.

### Class Development and Refactoring Features
ADT provides source code editing with specialized development tools:
- Code Completion: Triggered using `Ctrl + Space` to propose keywords, signatures, and context-sensitive components.
- Templates: Inserts standard code structures and blocks configured under IDE preferences.
- Mark Occurrences: Highlights all occurrences of an identifier across the active compilation unit when selected.
- Quick Fix and Refactoring: Triggered via `Ctrl + 1` or the Source menu, providing automated code transformations including renaming variables, extracting methods, and converting local variables to class attributes.

## Constructor Expressions and Syntax Features in Release 7.40
Release 7.40 of AS ABAP introduced constructor expressions using the general syntax `operator type( ... )`:
- `NEW`: Instantiates object instances and anonymous data objects. Replaces the procedural `CREATE OBJECT` statement and supports inline object creation.
- `VALUE`: Constructs complex data structures and populates internal tables.
- `REF`: Generates data references dynamically.
- `CONV`: Converts data types inline without helper variables.
- `CAST`: Executes up casts and down casts dynamically.
- `COND` and `SWITCH`: Implements conditional branching logic inline within assignment expressions.
- `DATA(...)`: Inline variable declaration operator that defines and types variables at the position of first assignment.

## Unified Modeling Language Object Diagrams
Object diagrams are structural UML diagrams that capture a snapshot of object instances and their relationships at a specific point during runtime execution. While class diagrams show static rules and potential connections, object diagrams illustrate actual instantiated structures, including recursive or nested object hierarchies.

An object instance in an object diagram is depicted as a rectangle containing the underlined object identifier and class name in the format `objectName : ClassName`. An optional lower compartment lists the current values of instance attributes at that runtime snapshot.

---

# Encapsulation and Implementation Hiding

## Procedural Programming Limitations

### Functional Decomposition and Step-Wise Refinement
Procedural software development utilizes functional decomposition, breaking complex program execution into subroutines and procedures through step-wise refinement. This approach focuses primarily on program actions rather than data modeling.

In complex procedural programs, functional decomposition results in centralized programs that manage numerous subroutines while retaining responsibility for global application data. Because subroutines share access to global memory, modifying the sequence of procedural calls can cause unintended side effects and data corruption. Supplying subroutines exclusively through extensive parameter lists results in tight coupling and cluttered procedural interfaces.

### Procedural Code Libraries in Function Groups
Function groups provide procedural modularization by grouping related function modules together with shared global data in a single function pool. However, the AS ABAP runtime allows only one instance of a function group to be loaded per internal session. 

Because function groups cannot be instantiated multiple times, developers cannot easily manage multiple concurrent data sets without implementing complex internal indexing. Consequently, function modules are typically designed as stateless routines that require calling programs to supply and track data structures externally. Exposing internal data layouts in function module signatures prevents developers from modifying storage structures without invalidating calling applications.

### Transition to Data Abstraction
Data abstraction models problem entities as Abstract Data Types (ADTs) that encapsulate state data together with the operations permitted on that data. Procedural programming separates data declarations from procedural logic, which leads to maintenance degradation as applications grow. Object-oriented classes resolve this limitation by binding data and operations into unified, encapsulated structures.

## Data Abstraction with Classes
Classes serve as Abstract Data Types by encapsulating attributes and methods within a single boundary. State data is maintained internally across method invocations, eliminating the requirement for calling programs to manage external state structures. Methods operate directly on internal attributes, simplifying parameter interfaces and ensuring that modifications to the internal data format remain isolated from external consumer code.

## Defining Component Visibilities

### Visibility Sections and Access Control
Component visibility determines the accessibility of class components from external contexts. ABAP Objects enforces visibility boundaries at compile time and runtime:
- Components declared in the `PUBLIC SECTION` represent the public interface and can be accessed by any consumer.
- Components declared in the `PRIVATE SECTION` are accessible exclusively by methods belonging to the defining class. Attempting to access private components from outside the class causes a compilation error.
- Components declared in the `PROTECTED SECTION` are accessible only by the defining class and its subclasses.

To protect object consistency, class attributes are typically declared in the `PRIVATE SECTION`. Access to private attributes is brokered via public accessor methods:
- Setter (Mutator) Methods: Receive input values and update private attributes after validating data integrity.
- Getter (Accessor) Methods: Return the current values of private attributes to external callers.

Attributes can also be declared in the `PUBLIC SECTION` using the `READ-ONLY` addition on the `DATA` statement. A `READ-ONLY` attribute can be read by external consumers but can only be modified by methods of the defining class.

### Friendship Relationships Between Classes
The friendship concept allows a class to grant unrestricted access to its `PRIVATE` and `PROTECTED` components to designated classes or interfaces without exposing those components publicly.

Friendship is declared in the class definition using the `FRIENDS` addition: `CLASS <class_name> DEFINITION FRIENDS <friend_class_1> <friend_class_2>`. In the Class Builder, friends are defined on the Friends tab.

Rules governing friendship in ABAP Objects:
- Friendship is one-way: Granting friendship to another class does not grant reciprocal access to the friend's protected or private components.
- Friendship cannot be inherited: Subclasses of a friend class do not automatically become friends of the granting class.
- Friendship is not transitive: A friend of a friend does not gain access permissions.
- Authorization is strictly granted by the defining class: A class cannot unilaterally declare itself a friend of another class.

When declaring a friend class that has not yet been defined in the program source code, a forward declaration must precede the granting class definition using the statement `CLASS <friend_class> DEFINITION DEFERRED`.

## Design by Contract
Design by Contract establishes a formal specification between a class and its consumers. The public interface defines the contract terms:
- Invariants: Rules defining consistent states that an object must satisfy throughout its lifecycle.
- Preconditions: Requirements that a caller must satisfy before invoking a method.
- Postconditions: Guarantees that the method fulfills upon successful completion.

Encapsulation ensures that external consumers cannot bypass contract preconditions by directly manipulating private state variables. Class developers can alter internal method algorithms provided the contractual obligations defined in the public signature are fulfilled.

## Unified Modeling Language Sequence Diagrams
A sequence diagram is a behavioral UML diagram that depicts interactions between objects arranged along a horizontal axis against time progressing down a vertical axis. 

Sequence diagram components include:
- Object Box: Represents an participating object instance.
- Lifeline: A vertical dashed line extending downward from an object box, representing the existence of the object over time.
- Found Message: An initial message arriving from an external source or user to start the sequence.
- Messages: Horizontal arrows connecting lifelines representing method invocations. Synchronous calls use solid arrowheads; return messages use dashed arrows.
- Activation Bar: A thin vertical rectangle placed on a lifeline indicating that the object is currently executing an operation.
- Self-Call: A message arrow that loops back to the same lifeline, indicating an internal helper method invocation. Nested activation bars represent stacked execution contexts.

---

# Object Initialization and Cleanup

## Object Creation Process and Memory Management
Execution of ABAP programs occurs within an internal session, which forms part of a call stack inside a main session. Main sessions reside within a user session (context) stored in the roll buffer of the shared memory area on the application server. The AS ABAP architecture operates a time-sharing model where user sessions roll in and roll out of dialog work processes.

To keep roll operations rapid, user sessions do not store heavy dynamic objects. When a program executes a `CREATE OBJECT` statement, the runtime environment:
1. Allocates contiguous memory for the object instance within the extended memory area outside the user session roll area.
2. Allocates an object header structure storing administrative metadata and runtime type references.
3. Initializes the instance attributes.
4. Executes the instance constructor method.
5. Returns the memory address of the object header to the target object reference variable.

Dynamic allocation introduces runtime overhead for locating contiguous memory blocks. Memory fragmentation can occur when numerous objects are dynamically created and discarded over time.

## Class and Instance Constructors

### Defining Instance Constructors
An instance constructor is an initialization method declared using the statement `METHODS constructor`. In the Class Builder, constructors are generated using the Constructor button.

Rules governing instance constructors:
- An instance constructor can only define `IMPORTING` parameters and `EXCEPTIONS`. It cannot define `EXPORTING`, `CHANGING`, or `RETURNING` parameters.
- Parameters can be passed by value or by reference.
- An instance constructor cannot be called explicitly via `CALL METHOD`. It is invoked exclusively by the runtime environment during execution of `CREATE OBJECT`.

### Runtime Behavior of Instance Constructors
The instance constructor ensures that an object enters a valid initial state before its reference is returned to the calling program. If initialization requirements are not met (such as missing database records or invalid importing parameter values), the constructor can raise an exception to abort object creation, preventing uninitialized or invalid instances from entering runtime execution.

### Class Constructors
A class constructor is a static initialization method declared using the statement `CLASS-METHODS class_constructor`. In the Class Builder, it is defined using the Class Constructor button.

Rules governing class constructors:
- A class constructor does not accept parameters of any kind and cannot raise exceptions.
- It is executed automatically by the runtime environment exactly once per internal session.
- The class constructor executes immediately before the class is accessed for the first time (such as calling a static method, accessing a static attribute, or instantiating the first object instance).
- A class constructor cannot directly access instance attributes or instance methods because it executes outside of any object context.

## Object-Creational Patterns

### Controlling Instantiation Context
The instantiation context of a class restricts where `CREATE OBJECT` statements can be executed. It is defined using the `CREATE` addition in the `CLASS DEFINITION` statement:
- `CREATE PUBLIC`: The class can be instantiated by any program or class. This is the default setting.
- `CREATE PROTECTED`: The class can only be instantiated by methods belonging to the class itself or its subclasses.
- `CREATE PRIVATE`: The class can only be instantiated by methods belonging to the class itself or its declared friends.
- `CREATE ABSTRACT`: Denotes an abstract class that cannot be directly instantiated.

In the Class Builder, this setting is configured using the Instantiation drop-down list on the Properties tab.

### The Singleton Pattern
The Singleton pattern ensures that only one instance of a class exists within an internal session and provides a centralized global access point to that instance.

Implementation in ABAP Objects requires:
1. Setting the class definition to `CREATE PRIVATE`.
2. Declaring a private static attribute of the class type to retain the singleton reference.
3. Declaring a private instance constructor to block external instantiation.
4. Declaring a public static factory method (such as `get_instance`) that evaluates the static reference. If the reference is not bound, the method executes `CREATE OBJECT` internally to instantiate the object and returns the bound reference to the caller.

### Factory Methods
ABAP Objects does not support method overloading (declaring multiple methods with the same name and differing parameter signatures). When an object must be instantiated through different data sources or configurations, relying on a single constructor with numerous optional parameters clutters the interface.

The Factory Method pattern resolves this by declaring public static methods that handle specific instantiation scenarios. Each factory method accepts only the parameters relevant to its specific context, executes internal instantiation, and returns the initialized object reference to the caller.

## Garbage Collection and Memory Reclamation
The ABAP runtime environment uses an automatic garbage collector to manage memory deallocation. Developers do not manually free object memory.

The garbage collector periodically inspects the extended memory area to identify orphaned object instances that no longer have active references pointing to them. When all object reference variables pointing to an instance are cleared using the `CLEAR` statement, assigned to different instances, or pass out of scope upon the termination of a method or subroutine, the object instance is flagged and its memory is reclaimed.

## Performance Optimization

### Design Considerations for Object Lifecycle
To optimize runtime efficiency when working with objects:
- Keep constructor logic minimal; delegate complex initialization tasks to private helper methods.
- For data transfer objects, implement a public reset method to clear instance attributes and recondition objects instead of creating new instances.
- Avoid cluttered constructor signatures by implementing focused factory methods.

### Lazy Initialization
Lazy initialization is a design technique where the allocation or loading of resource-intensive attributes is deferred until the attribute is explicitly requested via an accessor method. 

In composite objects containing nested structures or dependent data, loading all levels during constructor execution consumes memory and slows instantiation. Implementing lazy initialization checks whether the internal attribute is populated upon method invocation; if initial, the data is retrieved on demand.

### Object Reuse and Recycling
Repeatedly creating and discarding short-lived object instances inside processing loops causes performance degradation due to repeated memory allocation and garbage collection sweeps. Performance is optimized by recycling object instances: an object is instantiated outside the loop, its internal state is reinitialized on each iteration using a reset method, and the same instance is reused across iterations.

### Utilization of Class Attributes
When multiple object instances require access to identical, read-only data, storing that data in instance attributes duplicates memory usage across every instance. Defining shared data as a class attribute using `CLASS-DATA` allocates memory once per internal session, sharing the data across all instances.

## Unified Modeling Language State Machine Diagrams
A state machine diagram is a behavioral UML diagram that models the lifecycle of a single object, depicting the states an object transitions through in response to events.

Diagram components include:
- State: Represented by a rounded rectangle denoting a distinct operational condition of the object.
- Initial Pseudostate: A solid black circle indicating the starting point of the state machine.
- Transition: A directed arrow representing a change from one state to another.
- Transition Label: Formatted as `event [guard condition] / activity`. The event triggers the transition; the bracketed guard condition must evaluate to true for the transition to proceed; the activity specifies an action executed during the transition.
- Final State: A solid black circle enclosed within an outer ring, indicating the completion of the object lifecycle.

---

# Inheritance and Composition

## Generalization and Specialization

### Principles of Inheritance
Inheritance enables code reuse by structuring classes into hierarchies of generalized parent classes (superclasses) and specialized derived classes (subclasses). A subclass inherits the attributes, methods, and types of its superclass, and can expand functionality by defining additional components. 

Inheritance models an "is-a" relationship. In ABAP Objects, all classes implicitly derive from the predefined, empty base class named `OBJECT`. ABAP Objects supports single inheritance only: a class can inherit directly from only one superclass.

### Defining Inheritance in ABAP Objects
In ABAP Objects, an inheritance relationship is declared by adding the `INHERITING FROM` clause to the `CLASS DEFINITION` statement: `CLASS <subclass> DEFINITION INHERITING FROM <superclass>`.

In the Class Builder form-based editor, inheritance is configured using the Superclass, Undo Inheritance, and Change Inheritance buttons on the Properties tab:
- Superclass: Assigns a parent class to a subclass.
- Undo Inheritance: Removes the inheritance link, deleting all inherited components from the subclass.
- Change Inheritance: Reassigns the subclass to derive from a different superclass.

### Subclass Instantiation and Component Access
Subclasses are instantiated using the standard `CREATE OBJECT` statement. When instantiated, the subclass instance contains both its inherited components and its subclass-specific components. The runtime environment routes component calls dynamically: calls to inherited methods execute the superclass implementation, while calls to subclass-specific methods execute the subclass implementation.

### Propagation of Superclass Modifications
Inheritance maintains an active relationship throughout software maintenance. Modifying a superclass by adding new attributes, modifying public or protected method implementations, or altering signatures immediately propagates changes down the inheritance tree to all derived subclasses without requiring manual adjustments to the subclasses themselves.

## Inheriting Components

### Designing the Inheritance Interface
The inheritance interface comprises the components of a superclass accessible to its subclasses. Components declared in the `PROTECTED SECTION` are visible to the defining class and its subclasses, but remain invisible to external consumers.

According to the principle of least privilege, components should default to the `PRIVATE SECTION` unless subclass access is explicitly required. Protected components expose internal implementation details to derived classes; modifying protected components in a superclass can invalidate subclass implementations. When subclasses require access to private superclass attributes, protected getter and setter methods should be provided instead of exposing attributes directly.

### Visibility and Scoping of Inherited Instance Components
A subclass inherits all instance components from its superclass, but access depends on visibility:
- Public and protected components of the superclass are accessible within subclass methods.
- Private components of the superclass are inherited physically but are inaccessible within subclass methods.

Within a subclass, components of the immediate superclass can be addressed explicitly using the predefined pseudo-reference variable `super`. The `super` reference can access public and protected components of the superclass.

Public and protected components across an entire inheritance tree share a single internal namespace. A subclass cannot declare a component with the same name as an inherited public or protected component. Private components are exempt from this rule; a subclass can declare a private component with an identical name to a private component in its superclass without collision.

### Scoping and Access of Inherited Class Components
Subclasses inherit all public and protected class components (static attributes, constants, and static methods) from their superclasses. Static components belong to the inheritance hierarchy rather than a single instance. While static components can technically be addressed through the subclass name, standard practice requires addressing them using the defining class name via `<defining_class>=><component>` to preserve clarity.

### Method Redefinition
A subclass can alter the implementation of an inherited public or protected instance method using method redefinition. Method redefinition is declared in the subclass definition using the statement `METHODS <method_name> REDEFINITION`. In the Class Builder, redefinition is configured using the Redefine button on the Methods tab.

Rules governing method redefinition:
- The method signature cannot be altered. Parameter names, types, passing mechanisms, and visibilities remain identical to the superclass declaration.
- Static methods cannot be redefined.
- Private methods cannot be redefined because they are not visible to subclasses.
- Within the redefined implementation, the superclass implementation can be invoked using the statement `super-><method_name>( ... )`.

### Instance Constructors in Inheritance Hierarchies
Instance constructors are not inherited. Each class in an inheritance hierarchy defines its own constructor method independently.

When an instance constructor is implemented in a subclass:
- The subclass constructor must explicitly invoke the superclass constructor using `super->constructor( ... )` before accessing instance attributes or executing instance operations.
- The subclass constructor signature can introduce new parameters specific to the subclass, but must supply all non-optional importing parameters required by the superclass constructor.

### Class Constructors in Inheritance Hierarchies
Class constructors are independent across an inheritance hierarchy and cannot be inherited or redefined. 

When a subclass is accessed for the first time in an internal session, the ABAP runtime environment executes class constructors in a strict top-down sequence: the topmost superclass constructor executes first, followed down the hierarchy to the subclass constructor. This guarantees that static attributes of parent classes are initialized before child class execution begins.

## Abstract and Final Specifications

### Abstract Classes and Methods
Abstract components model incomplete design definitions:
- Abstract Methods: Declared using the `ABSTRACT` addition on the `METHODS` statement: `METHODS <method_name> ABSTRACT ...`. An abstract method defines a method signature without an implementation block.
- Abstract Classes: A class containing at least one abstract method must be declared abstract using the `ABSTRACT` addition on the `CLASS DEFINITION` statement: `CLASS <class_name> DEFINITION ABSTRACT ...`.

Rules governing abstract entities:
- Abstract classes cannot be instantiated using `CREATE OBJECT`.
- Abstract methods cannot be declared in the `PRIVATE SECTION` because they must be visible to subclasses for implementation.
- A non-abstract subclass inheriting from an abstract superclass must redefine and provide implementations for all inherited abstract methods. If any abstract method remains unimplemented, the subclass must also be declared abstract.

### Final Classes
A final class is a class that cannot be inherited. A class is declared as final by adding the `FINAL` keyword to the `CLASS DEFINITION` statement: `CLASS <class_name> DEFINITION FINAL ...`. For global classes, this is configured by selecting the Final checkbox on the Properties tab in the Class Builder. 

If a subclass attempts to inherit from a final class using `INHERITING FROM`, a compilation syntax error occurs. Final classes prevent further functional extension through inheritance.

### Final Methods
Individual methods can be declared as final without declaring the entire class as final. A method is finalized by adding the `FINAL` keyword to the `METHODS` statement: `METHODS <method_name> FINAL ...`. In the Class Builder, this is configured by selecting the Final checkbox in the method detail attributes.

When a method is declared as `FINAL`:
- The defining class can be inherited by subclasses.
- The final method cannot be redefined in any subclass. Attempting to specify the method in a `REDEFINITION` statement causes a syntax error.

## Composition Versus Inheritance
Inheritance models an "is-a" relationship, whereas composition models a "has-a" relationship. Composition reuses functionality by embedding an instance of an existing class as an attribute within another class.

Inheritance introduces tight coupling because changes to the superclass impact all derived subclasses, and subclasses inherit all public and protected components regardless of need. Composition provides greater design flexibility by allowing components to be swapped at runtime, keeping internal dependencies fully encapsulated within private attributes. Composition is preferred whenever the relationship between two entities is associative rather than a strict taxonomic specialization.

## Refactoring Tools in the ABAP Workbench and Eclipse
Refactoring improves internal software design without altering external runtime behavior. The ABAP development environment provides automated tools to support class refactoring:
- Refactoring Assistant (ABAP Workbench): Accessed in the Class Builder via `Utilities -> Refactoring -> Refactoring Assistant`. Provides a graphical drag-and-drop interface to move components, parameters, and methods between superclasses and subclasses, and to split or combine classes.
- Refactoring Tools (ADT in Eclipse): Accessed via the Source menu or the Quick Fix shortcut (`Ctrl + 1`). Provides automated operations for renaming identifiers across references, extracting code blocks into new methods, and converting local variables into class attributes.

## Unified Modeling Language Advanced Class Diagrams

### Generalizations in UML
Generalization represents inheritance in UML class diagrams. It is depicted as a solid line extending from the subclass to the superclass, terminating with an unfilled, closed triangle pointing toward the superclass.

### Dependencies and Composition in UML
A dependency represents a relationship where a change to one class can affect another, depicted as a dashed directed arrow pointing from the dependent class to the target class. 

Composition represents strong ownership and lifecycle dependence, depicted as an association line with a solid, filled diamond at the containing class end. If the containing object is destroyed, the composed member objects are destroyed as well.

### Abstract Classes and Methods in UML
In UML class diagrams, abstract classes and abstract methods are denoted by italicizing their names. Alternatively, abstract classes are indicated by prepending the stereotype `<<abstract>>` above the class name.

---

# Polymorphism

## Object Reference Assignments and Casting

### Static Types and Dynamic Types
Object reference variables operate with two distinct type classifications:
- Static Type: The type assigned to the reference variable when it is declared using `TYPE REF TO`. The static type is fixed at compile time and determines which components can be addressed through the reference variable using the object component selector (`->`).
- Dynamic Type: The actual class type of the object instance currently pointed to by the reference variable in memory at runtime. The dynamic type can change as different object instances are assigned to the reference variable.

An assignment between reference variables requires type compatibility. An assignment is valid if the static type of the target variable is identical to, or more general than, the dynamic type of the source variable.

### Narrowing Casts and Widening Casts
Casting operations realign static and dynamic reference types:
- Narrowing Cast (Up Cast): Occurs when assigning an object reference from a specific subclass type to a more general superclass reference variable. Because a subclass instance contains all components of its superclass, an up cast is inherently type-safe and can be performed implicitly using the standard assignment operator (`=`). An up cast can also be executed during instantiation using `CREATE OBJECT oref TYPE subclass` or using the constructor operator `CAST superclass_type( subclass_ref )`. A narrowing cast restricts compile-time component visibility to the components defined in the target static type.
- Widening Cast (Down Cast): Occurs when assigning an object reference from a general superclass reference variable to a more specific subclass reference variable. A widening cast cannot be verified at compile time because the runtime object may not match the specialized target type. Therefore, a down cast must be explicitly declared using the casting operator (`?=`) or the constructor operator `CAST subclass_type( superclass_ref )`. 

At runtime, the environment verifies whether the dynamic type of the source reference matches or derives from the static type of the target reference. If the types are incompatible, the runtime environment aborts the assignment and raises the catchable class-based exception `CX_SY_MOVE_CAST_ERROR`.

## Dynamic Method Call Binding
Dynamic method call binding dispatches method execution at runtime based on the dynamic type of the object instance rather than the static type of the reference variable.

When a method is invoked through a generic superclass reference variable, the runtime environment inspects the object header to determine the concrete dynamic class. If the method has been redefined in the subclass, execution is bound dynamically to the redefined subclass implementation. This allows programs to process heterogeneous collections of subclass instances generically without containing conditional type-checking logic.

## Interfaces

### Single Inheritance and Interface Inheritance
ABAP Objects enforces a single inheritance model for classes to prevent ambiguities such as the diamond problem, where a class inherits conflicting implementations of the same method from multiple parent paths. 

Interfaces overcome single inheritance limitations by providing interface inheritance without implementation inheritance. An interface is an independent repository artifact that defines a contract consisting of component signatures without any implementation. A class can implement multiple independent interfaces, enabling the class to assume multiple polymorphic types across unrelated inheritance hierarchies.

### Defining Interfaces
Local interfaces are declared using the `INTERFACE ... ENDINTERFACE` statement block. Global interfaces are created in the Class Builder (Transaction `SE24` or `SE80`) and stored as repository objects with prefix `ZIF_` or `IF_`.

Rules governing interface definitions:
- Interfaces do not have visibility sections (`PUBLIC`, `PROTECTED`, or `PRIVATE`). All interface components are implicitly public.
- Interfaces can define attributes, methods, events, and data types.
- Interfaces do not have implementation blocks. Interface methods contain signatures only.

### Implementing Interfaces
A class implements an interface by declaring the `INTERFACES <interface_name>` statement within its `PUBLIC SECTION`. In the Class Builder, interfaces are assigned on the Interfaces tab.

When a class implements an interface:
- All methods declared in the interface must be implemented within the `CLASS ... IMPLEMENTATION` block of the class, unless declared as optional in the interface definition.
- Interface components are addressed in the class definition and implementation using the interface component selector operator (`~`) in the format `<interface_name>~<component_name>`.
- In Release 7.40 and higher, interface methods can be defined with the `DEFAULT` addition on the `METHODS` statement:
  - `DEFAULT IGNORE`: Allows implementing classes to omit the method implementation without raising a syntax error. At runtime, calling the unimplemented method produces no operation.
  - `DEFAULT FAIL`: Requires implementation; calling an unimplemented method at runtime raises a fatal runtime error.

### Polymorphism with Interface References
Interface reference variables are declared using the statement `DATA iref TYPE REF TO <interface_name>`. 

An interface reference variable can point to any object instance whose class implements that interface. Assigning an object instance to an interface reference variable executes an implicit narrowing cast. Through the interface reference variable, the caller can invoke any component defined in the interface directly using `iref->component` without specifying the interface component selector (`~`). Dynamic binding ensures the method implementation provided by the concrete implementing class executes.

### Compound and Nested Interfaces
Interfaces can be nested within other interfaces using the `INTERFACES <component_interface>` statement inside an interface definition. The containing interface is termed a compound (nested) interface, and the embedded interface is termed a component interface.

Rules governing nested interfaces:
- Component interfaces exist at the same hierarchical level within the compound interface; multiple nesting of the same interface resolves to a single instance.
- Components of a component interface are addressed using the interface component selector: `<component_interface>~<component_name>`.
- Aliases can be declared within the compound interface using the statement `ALIASES <alias_name> FOR <component_interface>~<component_name>`. Aliases expose nested components as direct members of the compound interface.
- An object reference variable typed with a compound interface can be assigned to a reference variable typed with one of its component interfaces via a narrowing cast.

### Interface Usage Scenarios
Interfaces are used in specific architectural scenarios:
- Secondary Roles and Cross-Cutting Concerns: While class inheritance models primary taxonomy, interfaces model secondary roles or peripheral capabilities (such as comparable, serializable, or workflow-enabled objects) that span unrelated class hierarchies.
- Implementation Decoupling via Factories: System frameworks decouple consumers from concrete implementations by defining public APIs entirely through interfaces. Concrete classes implementing the interfaces are instantiated internally via factory classes and returned to consumers as interface references, shielding consumers from underlying kernel or database dependencies.

## Unified Modeling Language Interface Notation

### Interface Representation in UML
In UML class diagrams, an interface is depicted as a standard class rectangle containing the stereotype `<<interface>>` above the interface name. Attribute and operation compartments follow standard class diagram notations.

### Interface Provision and Requirement Relationships
The relationship between a class and an interface is modeled in two ways:
- Providing (Implementing) Relationship: Depicted as a dashed line extending from the implementing class to the interface rectangle, terminating with an unfilled closed triangle pointing at the interface.
- Requiring (Dependency) Relationship: Depicted as a dashed line with an open arrow pointing from the client class to the required interface, indicating that the client class operates through that interface.

### Static Component Representation in UML
Static attributes and static methods belonging to a class or an interface are represented in UML diagrams by underlining the component name within the respective compartment.