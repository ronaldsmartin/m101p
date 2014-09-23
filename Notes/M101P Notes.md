M101P Notes
===========

Week 01
-------

## Logistics
Only Homework and Final Exam count (50% each)
65% = Passing
Lowest Homework Dropped

## What is Mongo?
Document-based, JSON-like, schemaless database

### Relative to Relational
Scalable & High-Performance with lots of functionality
Does not support Joins or Transactions


Week 02
-------

## Find & FindOne
`db.(collection name).findOne(obj1, obj2)`

Returns objects in the collection whose fields match the fields specified in first param
Returns only the fields specifed in the optional second parameter:
* `_id` is shown by default
* fields can be toggled on/off by using true/false or 1/0, e.g. `{_id:false, name:1}`

Field matching is polymorphic over array and non-array types in a non-recursive fashion.
e.g. `db.(collection name).findOne({name: "me"})` will match documents whose `name` field is a string with value `"me"` and also match documents whose `name` field is an array that contains the string `"me"`.

## Finding ranges with $gt and $lt
Use operators in subdocuments to match ranges instead of constant values.
e.g. `db.collection.find( {score: { $gt: 95 } } )` finds objects with `score > 95`.

Conversely, use other operators to find objects values in different ranges
e.g. `db.collection.find( {score: { $gt: 95, $lte: 98 } } )` finds objects with `95 < score <= 98`.

### Operators:
`$gt`, `$gte`, `$lt`, `$lte` for >, >=, <, <=.

### Comparisons Do Not Span Data Types
While Mongo is schemaless, using these comparison operators will not return results of a different datatype.
E.g.: `db.collection.find( {score: { $gt: 95 } } )` will not return any objects whose score field is a string.

*Note:* Lexographic comparison conforms to UTF-8 byte encodings. Locale aware implementations are planned.


## Filtering results by type and field existence
### $exists
The operator `$exists` can be used to filter documents with specific fields.
e.g.: `db.collection.find( {name: {$exists:true} } )` finds documents that have a field called `name`.

### $type
The operator `$type` can be used to filter documents whose fields have a specific type. Types are specified by integer codes in the BSON spec. String = 2.
e.g.: `db.collection.find( {name: {$type:2} } )` finds documents that have a string in the field called `name`.

### $regex
The operator `$regex` can be used to filter documents using Perl-style regular expressions. 
e.g.: `db.collection.find( {name: {$regex:"e$"} } )` finds documents that have a string in the field called `name` ending with the letter e.
e.g.: `db.collection.find( {name: {$regex:"^A"} } )` finds documents that have a string in the field called `name` beginning with a capital A.

## Prefix operators $or and $and
### Union via $or
e.g.: `db.collection.find( {$or: [{$regex:"e$"}, {$regex:"^A"}] } )` finds documents that have a string in the field called `name` ending with the letter e *or* beginning with a capital A.

### Intersection via $and
This is less common because you can already combine queries for one field.

e.g.: `db.collection.find( {$and: [{$regex:"e$"}, {$regex:"^A"}] } )` finds documents that have a string in the field called `name` ending with the letter e *and* beginning with a capital A.

### Sidenote: Notes on the interpreter
The interpreter will highlight matching parentheses or brackets in dark blue.

On receiving input with unmatched parentheses, the interpreter will display `...` to enable you to close the parentheses. If you cannot close the parens, press `return` twice.


## Array element matching with $in and $all
### $all
Using `$all` checks if a field is a superset of members specified in the query.
e.g.: `db.collection.find( {favorites: {$all: ["hello", "world"] } } )` returns items whose `favorites` field is an array that contains `"hello"` and `"world"` in any order.

### $in
Using `$all` checks if a field contains a subset of members specified in the query.
e.g.: `db.collection.find( {favorites: {$in: ["hello", "world"] } } )` returns items whose `favorites` field is an array that contains `"hello"` or (inclusive) `"world"`.

## Dot Notation
To search nested documents, you can use dot-notation.

Case: collection includes `{name: "Name", email: {work:"address1", home:"address2"}}`
Because of JavaScript equality-checking, the following queries will not match:
* `db.collection.find( { email: {home:"address2", work:"address1"} } )` (order invariance is not preserved)
* `db.collection.find( { email: {home:"address2"} } )` (`{home:"address2"} != {work:"address1", home:"address2"}`)

Instead, you can use dot-notation:
```javascript
  db.collection.find( {"email.work": "address" } )
```
which will match the object successfully.


## Cursors
`db.collection.find()` creates a cursor that you can bind to a variable. Use `null` to prevent the default behavior of printing out all results.
e.g. `cursor = db.collection.find(); null;`

From here, you can call methods on the cursor.
* `cursor.hasNext()`
* `cursor.next()` get the next matching object
* `cursor.limit(numberOfEntries); null;` truncates the match result to this many entries and return the new cursor
* `cursor.sort({name:-1}); null;` reverse order by name
* `cursor.skip(numToSkip); null;` skip a number of documents

Since many of these methods return the new cursor, you can chain them.
e.g.: `db.collection.find().limit(50).skip(10)`


## Counting
Count matches using the count() method.
e.g. `db.collection.count({type: "exam"})` returns the number of documents with `"exam"` in the `type` field.
 
## Updating Documents

### update() for wholesale updating of a document
The `update()` method on collections lets you replace matches.
e.g.: `db.collection.update({name: "Smith"}, {hello: "world"})` finds any document with `"Smith"` in the `name` field and replaces it with the document `{hello: "world"}`, retaining the `_id` field.

### Using operators for partial document updates
#### Setting/creating fields
The `$set` operator allows you to update only specific fields instead of forcing wholesale replacement.
e.g.: `db.collection.update({name: "Smith"}, {$set: {age: 10}})` finds the first document with `name` `"Smith"` and sets *only* the `age` field to `10`, creating this field if necessary.

#### Incrementing fields
The `$inc` operator lets you increment fields.
e.g.: `db.collection.update({name: "Smith"}, {$inc: {age: num}})` finds the first document with `name` `"Smith"` and increments *only* the `age` field by `num`, creating this field with value `num` if necessary.

#### Remove fields
Use the `$unset` operator to remove specific fields.
e.g.: `db.collection.update({name: "Smith"}, {$unset: {age: 1}})` finds the first document with `name` `"Smith"` and deletes *only* the `age` field. The argument to `age` is ignored.

### Updating arrays
The previous operators can be combined with dot-notation to modify fields that are arrays.
e.g.: `db.arrays.update({_id: 0}, {$set: {"array.3": 5}})` finds the document with `_id` `0`, accesses the element with index 3 in its `array` field, and sets this element to 5.

#### Push and pop
Use `$push` to append elements to arrays and `$pop` to pop the first element of the array.
e.g.: `db.arrays.update({_id: 0}, {$push: {array: 5}})` finds the document with `_id` `0`, and adds the element 5 to the end of its `array` field.

Use `$pushAll` to concatenate an array.
e.g.: `db.arrays.update({_id: 0}, {$pushAll: {array: [7, 8, 9]}})` finds the document with `_id` `0`, and adds the elements `[7, 8, 9]` to the of its `array` field.

Use `$pull` and `$pullAll` to remove elements from an array.
e.g.: `db.arrays.update({_id: 0}, {$pullAll: {array: [7, 8, 9]}})` finds the document with `_id` `0`, and removes all instances of the elements `7`, `8`, or `9` from the `array` field.

Use `$addToSet` to add elements to an array, preventing duplicate additions.
e.g.: `db.arrays.update({_id: 0}, {$addToSet: {array: 5}})` finds the document with `_id` `0`, and adds the element `5` to the field `array` iff it `5` is not already a member in `array`.

### Upsert
Add `{upsert: true}` to update an existing field in a document or insert a new document if such a document doesn't exist.
e.g.: `db.collection.update({name: "Smith"}, {$set: {age: 10}}, {upsert: true})` finds a document with `name` `"Smith"` and sets *only* the `age` field to `10`, creating a new document with this criteria if necessary.

### Multi-Update
Add `{multi: true}` tag to let update() affect multiple documents
e.g.: `db.collection.update({name: "Smith"}, {$set: {age: 10}}, {multi: true})` finds all documents with `name` `"Smith"` and sets *only* the `age` field to `10`.

**REWATCH THIS TO UNDERSTAND CONCURRENCY IMPLICATIONS**


## Removing Documents
Use `remove(document)` to remove a document. Use `drop()` to remove all documents from a collection. Dropping is much faster, but removes all metadata.