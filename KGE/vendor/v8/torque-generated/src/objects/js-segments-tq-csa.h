#ifndef V8_GEN_TORQUE_GENERATED_SRC_OBJECTS_JS_SEGMENTS_TQ_CSA_H_
#define V8_GEN_TORQUE_GENERATED_SRC_OBJECTS_JS_SEGMENTS_TQ_CSA_H_
#include "src/builtins/torque-csa-header-includes.h"

namespace v8 {
namespace internal {
TNode<JSSegments> Cast_JSSegments_0(compiler::CodeAssemblerState* state_, TNode<HeapObject> p_obj, compiler::CodeAssemblerLabel* label_CastError);
TNode<Foreign> LoadJSSegmentsIcuBreakIterator_0(compiler::CodeAssemblerState* state_, TNode<JSSegments> p_o);
void StoreJSSegmentsIcuBreakIterator_0(compiler::CodeAssemblerState* state_, TNode<JSSegments> p_o, TNode<Foreign> p_v);
TNode<Foreign> LoadJSSegmentsUnicodeString_0(compiler::CodeAssemblerState* state_, TNode<JSSegments> p_o);
void StoreJSSegmentsUnicodeString_0(compiler::CodeAssemblerState* state_, TNode<JSSegments> p_o, TNode<Foreign> p_v);
TNode<Smi> LoadJSSegmentsFlags_0(compiler::CodeAssemblerState* state_, TNode<JSSegments> p_o);
void StoreJSSegmentsFlags_0(compiler::CodeAssemblerState* state_, TNode<JSSegments> p_o, TNode<Smi> p_v);
TNode<JSSegments> DownCastForTorqueClass_JSSegments_0(compiler::CodeAssemblerState* state_, TNode<HeapObject> p_o, compiler::CodeAssemblerLabel* label_CastError);
} // namespace internal
} // namespace v8
#endif // V8_GEN_TORQUE_GENERATED_SRC_OBJECTS_JS_SEGMENTS_TQ_CSA_H_
