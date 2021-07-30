#ifndef V8_GEN_TORQUE_GENERATED_SRC_OBJECTS_JS_COLLATOR_TQ_CSA_H_
#define V8_GEN_TORQUE_GENERATED_SRC_OBJECTS_JS_COLLATOR_TQ_CSA_H_
#include "src/builtins/torque-csa-header-includes.h"

namespace v8 {
namespace internal {
TNode<JSCollator> Cast_JSCollator_0(compiler::CodeAssemblerState* state_, TNode<HeapObject> p_obj, compiler::CodeAssemblerLabel* label_CastError);
TNode<Foreign> LoadJSCollatorIcuCollator_0(compiler::CodeAssemblerState* state_, TNode<JSCollator> p_o);
void StoreJSCollatorIcuCollator_0(compiler::CodeAssemblerState* state_, TNode<JSCollator> p_o, TNode<Foreign> p_v);
TNode<HeapObject> LoadJSCollatorBoundCompare_0(compiler::CodeAssemblerState* state_, TNode<JSCollator> p_o);
void StoreJSCollatorBoundCompare_0(compiler::CodeAssemblerState* state_, TNode<JSCollator> p_o, TNode<HeapObject> p_v);
TNode<String> LoadJSCollatorLocale_0(compiler::CodeAssemblerState* state_, TNode<JSCollator> p_o);
void StoreJSCollatorLocale_0(compiler::CodeAssemblerState* state_, TNode<JSCollator> p_o, TNode<String> p_v);
TNode<JSCollator> DownCastForTorqueClass_JSCollator_0(compiler::CodeAssemblerState* state_, TNode<HeapObject> p_o, compiler::CodeAssemblerLabel* label_CastError);
} // namespace internal
} // namespace v8
#endif // V8_GEN_TORQUE_GENERATED_SRC_OBJECTS_JS_COLLATOR_TQ_CSA_H_
