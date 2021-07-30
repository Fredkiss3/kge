#ifndef V8_GEN_TORQUE_GENERATED_SRC_OBJECTS_JS_DISPLAY_NAMES_TQ_CSA_H_
#define V8_GEN_TORQUE_GENERATED_SRC_OBJECTS_JS_DISPLAY_NAMES_TQ_CSA_H_
#include "src/builtins/torque-csa-header-includes.h"

namespace v8 {
namespace internal {
TNode<JSDisplayNames> Cast_JSDisplayNames_0(compiler::CodeAssemblerState* state_, TNode<HeapObject> p_obj, compiler::CodeAssemblerLabel* label_CastError);
TNode<Foreign> LoadJSDisplayNamesInternal_0(compiler::CodeAssemblerState* state_, TNode<JSDisplayNames> p_o);
void StoreJSDisplayNamesInternal_0(compiler::CodeAssemblerState* state_, TNode<JSDisplayNames> p_o, TNode<Foreign> p_v);
TNode<Smi> LoadJSDisplayNamesFlags_0(compiler::CodeAssemblerState* state_, TNode<JSDisplayNames> p_o);
void StoreJSDisplayNamesFlags_0(compiler::CodeAssemblerState* state_, TNode<JSDisplayNames> p_o, TNode<Smi> p_v);
TNode<JSDisplayNames> DownCastForTorqueClass_JSDisplayNames_0(compiler::CodeAssemblerState* state_, TNode<HeapObject> p_o, compiler::CodeAssemblerLabel* label_CastError);
} // namespace internal
} // namespace v8
#endif // V8_GEN_TORQUE_GENERATED_SRC_OBJECTS_JS_DISPLAY_NAMES_TQ_CSA_H_
