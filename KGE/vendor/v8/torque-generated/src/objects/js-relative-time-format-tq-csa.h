#ifndef V8_GEN_TORQUE_GENERATED_SRC_OBJECTS_JS_RELATIVE_TIME_FORMAT_TQ_CSA_H_
#define V8_GEN_TORQUE_GENERATED_SRC_OBJECTS_JS_RELATIVE_TIME_FORMAT_TQ_CSA_H_
#include "src/builtins/torque-csa-header-includes.h"

namespace v8 {
namespace internal {
TNode<JSRelativeTimeFormat> Cast_JSRelativeTimeFormat_0(compiler::CodeAssemblerState* state_, TNode<HeapObject> p_obj, compiler::CodeAssemblerLabel* label_CastError);
TNode<String> LoadJSRelativeTimeFormatLocale_0(compiler::CodeAssemblerState* state_, TNode<JSRelativeTimeFormat> p_o);
void StoreJSRelativeTimeFormatLocale_0(compiler::CodeAssemblerState* state_, TNode<JSRelativeTimeFormat> p_o, TNode<String> p_v);
TNode<String> LoadJSRelativeTimeFormatNumberingSystem_0(compiler::CodeAssemblerState* state_, TNode<JSRelativeTimeFormat> p_o);
void StoreJSRelativeTimeFormatNumberingSystem_0(compiler::CodeAssemblerState* state_, TNode<JSRelativeTimeFormat> p_o, TNode<String> p_v);
TNode<Foreign> LoadJSRelativeTimeFormatIcuFormatter_0(compiler::CodeAssemblerState* state_, TNode<JSRelativeTimeFormat> p_o);
void StoreJSRelativeTimeFormatIcuFormatter_0(compiler::CodeAssemblerState* state_, TNode<JSRelativeTimeFormat> p_o, TNode<Foreign> p_v);
TNode<Smi> LoadJSRelativeTimeFormatFlags_0(compiler::CodeAssemblerState* state_, TNode<JSRelativeTimeFormat> p_o);
void StoreJSRelativeTimeFormatFlags_0(compiler::CodeAssemblerState* state_, TNode<JSRelativeTimeFormat> p_o, TNode<Smi> p_v);
TNode<JSRelativeTimeFormat> DownCastForTorqueClass_JSRelativeTimeFormat_0(compiler::CodeAssemblerState* state_, TNode<HeapObject> p_o, compiler::CodeAssemblerLabel* label_CastError);
} // namespace internal
} // namespace v8
#endif // V8_GEN_TORQUE_GENERATED_SRC_OBJECTS_JS_RELATIVE_TIME_FORMAT_TQ_CSA_H_
