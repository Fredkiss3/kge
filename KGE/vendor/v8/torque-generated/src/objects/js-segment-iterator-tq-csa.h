#ifndef V8_GEN_TORQUE_GENERATED_SRC_OBJECTS_JS_SEGMENT_ITERATOR_TQ_CSA_H_
#define V8_GEN_TORQUE_GENERATED_SRC_OBJECTS_JS_SEGMENT_ITERATOR_TQ_CSA_H_
#include "src/builtins/torque-csa-header-includes.h"

namespace v8 {
namespace internal {
TNode<JSSegmentIterator> Cast_JSSegmentIterator_0(compiler::CodeAssemblerState* state_, TNode<HeapObject> p_obj, compiler::CodeAssemblerLabel* label_CastError);
TNode<Foreign> LoadJSSegmentIteratorIcuBreakIterator_0(compiler::CodeAssemblerState* state_, TNode<JSSegmentIterator> p_o);
void StoreJSSegmentIteratorIcuBreakIterator_0(compiler::CodeAssemblerState* state_, TNode<JSSegmentIterator> p_o, TNode<Foreign> p_v);
TNode<Foreign> LoadJSSegmentIteratorUnicodeString_0(compiler::CodeAssemblerState* state_, TNode<JSSegmentIterator> p_o);
void StoreJSSegmentIteratorUnicodeString_0(compiler::CodeAssemblerState* state_, TNode<JSSegmentIterator> p_o, TNode<Foreign> p_v);
TNode<Smi> LoadJSSegmentIteratorFlags_0(compiler::CodeAssemblerState* state_, TNode<JSSegmentIterator> p_o);
void StoreJSSegmentIteratorFlags_0(compiler::CodeAssemblerState* state_, TNode<JSSegmentIterator> p_o, TNode<Smi> p_v);
TNode<JSSegmentIterator> DownCastForTorqueClass_JSSegmentIterator_0(compiler::CodeAssemblerState* state_, TNode<HeapObject> p_o, compiler::CodeAssemblerLabel* label_CastError);
} // namespace internal
} // namespace v8
#endif // V8_GEN_TORQUE_GENERATED_SRC_OBJECTS_JS_SEGMENT_ITERATOR_TQ_CSA_H_
