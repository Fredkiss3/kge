#ifndef V8_GEN_TORQUE_GENERATED_SRC_OBJECTS_JS_SEGMENTER_TQ_CSA_H_
#define V8_GEN_TORQUE_GENERATED_SRC_OBJECTS_JS_SEGMENTER_TQ_CSA_H_
#include "src/builtins/torque-csa-header-includes.h"

namespace v8 {
namespace internal {
TNode<JSSegmenter> Cast_JSSegmenter_0(compiler::CodeAssemblerState* state_, TNode<HeapObject> p_obj, compiler::CodeAssemblerLabel* label_CastError);
TNode<String> LoadJSSegmenterLocale_0(compiler::CodeAssemblerState* state_, TNode<JSSegmenter> p_o);
void StoreJSSegmenterLocale_0(compiler::CodeAssemblerState* state_, TNode<JSSegmenter> p_o, TNode<String> p_v);
TNode<Foreign> LoadJSSegmenterIcuBreakIterator_0(compiler::CodeAssemblerState* state_, TNode<JSSegmenter> p_o);
void StoreJSSegmenterIcuBreakIterator_0(compiler::CodeAssemblerState* state_, TNode<JSSegmenter> p_o, TNode<Foreign> p_v);
TNode<Smi> LoadJSSegmenterFlags_0(compiler::CodeAssemblerState* state_, TNode<JSSegmenter> p_o);
void StoreJSSegmenterFlags_0(compiler::CodeAssemblerState* state_, TNode<JSSegmenter> p_o, TNode<Smi> p_v);
TNode<JSSegmenter> DownCastForTorqueClass_JSSegmenter_0(compiler::CodeAssemblerState* state_, TNode<HeapObject> p_o, compiler::CodeAssemblerLabel* label_CastError);
} // namespace internal
} // namespace v8
#endif // V8_GEN_TORQUE_GENERATED_SRC_OBJECTS_JS_SEGMENTER_TQ_CSA_H_
