#ifndef V8_GEN_TORQUE_GENERATED_SRC_OBJECTS_JS_NUMBER_FORMAT_TQ_CSA_H_
#define V8_GEN_TORQUE_GENERATED_SRC_OBJECTS_JS_NUMBER_FORMAT_TQ_CSA_H_
#include "src/builtins/torque-csa-header-includes.h"

namespace v8 {
namespace internal {
TNode<JSNumberFormat> Cast_JSNumberFormat_0(compiler::CodeAssemblerState* state_, TNode<HeapObject> p_obj, compiler::CodeAssemblerLabel* label_CastError);
TNode<String> LoadJSNumberFormatLocale_0(compiler::CodeAssemblerState* state_, TNode<JSNumberFormat> p_o);
void StoreJSNumberFormatLocale_0(compiler::CodeAssemblerState* state_, TNode<JSNumberFormat> p_o, TNode<String> p_v);
TNode<Foreign> LoadJSNumberFormatIcuNumberFormatter_0(compiler::CodeAssemblerState* state_, TNode<JSNumberFormat> p_o);
void StoreJSNumberFormatIcuNumberFormatter_0(compiler::CodeAssemblerState* state_, TNode<JSNumberFormat> p_o, TNode<Foreign> p_v);
TNode<HeapObject> LoadJSNumberFormatBoundFormat_0(compiler::CodeAssemblerState* state_, TNode<JSNumberFormat> p_o);
void StoreJSNumberFormatBoundFormat_0(compiler::CodeAssemblerState* state_, TNode<JSNumberFormat> p_o, TNode<HeapObject> p_v);
TNode<JSNumberFormat> DownCastForTorqueClass_JSNumberFormat_0(compiler::CodeAssemblerState* state_, TNode<HeapObject> p_o, compiler::CodeAssemblerLabel* label_CastError);
} // namespace internal
} // namespace v8
#endif // V8_GEN_TORQUE_GENERATED_SRC_OBJECTS_JS_NUMBER_FORMAT_TQ_CSA_H_
