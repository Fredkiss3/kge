#ifndef V8_GEN_TORQUE_GENERATED_SRC_OBJECTS_JS_PLURAL_RULES_TQ_CSA_H_
#define V8_GEN_TORQUE_GENERATED_SRC_OBJECTS_JS_PLURAL_RULES_TQ_CSA_H_
#include "src/builtins/torque-csa-header-includes.h"

namespace v8 {
namespace internal {
TNode<JSPluralRules> Cast_JSPluralRules_0(compiler::CodeAssemblerState* state_, TNode<HeapObject> p_obj, compiler::CodeAssemblerLabel* label_CastError);
TNode<String> LoadJSPluralRulesLocale_0(compiler::CodeAssemblerState* state_, TNode<JSPluralRules> p_o);
void StoreJSPluralRulesLocale_0(compiler::CodeAssemblerState* state_, TNode<JSPluralRules> p_o, TNode<String> p_v);
TNode<Smi> LoadJSPluralRulesFlags_0(compiler::CodeAssemblerState* state_, TNode<JSPluralRules> p_o);
void StoreJSPluralRulesFlags_0(compiler::CodeAssemblerState* state_, TNode<JSPluralRules> p_o, TNode<Smi> p_v);
TNode<Foreign> LoadJSPluralRulesIcuPluralRules_0(compiler::CodeAssemblerState* state_, TNode<JSPluralRules> p_o);
void StoreJSPluralRulesIcuPluralRules_0(compiler::CodeAssemblerState* state_, TNode<JSPluralRules> p_o, TNode<Foreign> p_v);
TNode<Foreign> LoadJSPluralRulesIcuNumberFormatter_0(compiler::CodeAssemblerState* state_, TNode<JSPluralRules> p_o);
void StoreJSPluralRulesIcuNumberFormatter_0(compiler::CodeAssemblerState* state_, TNode<JSPluralRules> p_o, TNode<Foreign> p_v);
TNode<JSPluralRules> DownCastForTorqueClass_JSPluralRules_0(compiler::CodeAssemblerState* state_, TNode<HeapObject> p_o, compiler::CodeAssemblerLabel* label_CastError);
} // namespace internal
} // namespace v8
#endif // V8_GEN_TORQUE_GENERATED_SRC_OBJECTS_JS_PLURAL_RULES_TQ_CSA_H_
