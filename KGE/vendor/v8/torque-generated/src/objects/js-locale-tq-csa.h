#ifndef V8_GEN_TORQUE_GENERATED_SRC_OBJECTS_JS_LOCALE_TQ_CSA_H_
#define V8_GEN_TORQUE_GENERATED_SRC_OBJECTS_JS_LOCALE_TQ_CSA_H_
#include "src/builtins/torque-csa-header-includes.h"

namespace v8 {
namespace internal {
TNode<JSLocale> Cast_JSLocale_0(compiler::CodeAssemblerState* state_, TNode<HeapObject> p_obj, compiler::CodeAssemblerLabel* label_CastError);
TNode<Foreign> LoadJSLocaleIcuLocale_0(compiler::CodeAssemblerState* state_, TNode<JSLocale> p_o);
void StoreJSLocaleIcuLocale_0(compiler::CodeAssemblerState* state_, TNode<JSLocale> p_o, TNode<Foreign> p_v);
TNode<JSLocale> DownCastForTorqueClass_JSLocale_0(compiler::CodeAssemblerState* state_, TNode<HeapObject> p_o, compiler::CodeAssemblerLabel* label_CastError);
} // namespace internal
} // namespace v8
#endif // V8_GEN_TORQUE_GENERATED_SRC_OBJECTS_JS_LOCALE_TQ_CSA_H_
