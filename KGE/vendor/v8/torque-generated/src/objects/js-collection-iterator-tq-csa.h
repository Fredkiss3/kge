#ifndef V8_GEN_TORQUE_GENERATED_SRC_OBJECTS_JS_COLLECTION_ITERATOR_TQ_CSA_H_
#define V8_GEN_TORQUE_GENERATED_SRC_OBJECTS_JS_COLLECTION_ITERATOR_TQ_CSA_H_
#include "src/builtins/torque-csa-header-includes.h"

namespace v8 {
namespace internal {
TNode<JSCollectionIterator> Cast_JSCollectionIterator_0(compiler::CodeAssemblerState* state_, TNode<HeapObject> p_obj, compiler::CodeAssemblerLabel* label_CastError);
TNode<Object> LoadJSCollectionIteratorTable_0(compiler::CodeAssemblerState* state_, TNode<JSCollectionIterator> p_o);
void StoreJSCollectionIteratorTable_0(compiler::CodeAssemblerState* state_, TNode<JSCollectionIterator> p_o, TNode<Object> p_v);
TNode<Object> LoadJSCollectionIteratorIndex_0(compiler::CodeAssemblerState* state_, TNode<JSCollectionIterator> p_o);
void StoreJSCollectionIteratorIndex_0(compiler::CodeAssemblerState* state_, TNode<JSCollectionIterator> p_o, TNode<Object> p_v);
TNode<JSCollectionIterator> DownCastForTorqueClass_JSCollectionIterator_0(compiler::CodeAssemblerState* state_, TNode<HeapObject> p_o, compiler::CodeAssemblerLabel* label_CastError);
} // namespace internal
} // namespace v8
#endif // V8_GEN_TORQUE_GENERATED_SRC_OBJECTS_JS_COLLECTION_ITERATOR_TQ_CSA_H_
