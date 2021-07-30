#ifndef V8_GEN_TORQUE_GENERATED_SRC_OBJECTS_JS_LIST_FORMAT_TQ_CSA_H_
#define V8_GEN_TORQUE_GENERATED_SRC_OBJECTS_JS_LIST_FORMAT_TQ_CSA_H_
#include "src/builtins/torque-csa-header-includes.h"

namespace v8 {
namespace internal {
TNode<JSListFormat> Cast_JSListFormat_0(compiler::CodeAssemblerState* state_, TNode<HeapObject> p_obj, compiler::CodeAssemblerLabel* label_CastError);
TNode<String> LoadJSListFormatLocale_0(compiler::CodeAssemblerState* state_, TNode<JSListFormat> p_o);
void StoreJSListFormatLocale_0(compiler::CodeAssemblerState* state_, TNode<JSListFormat> p_o, TNode<String> p_v);
TNode<Foreign> LoadJSListFormatIcuFormatter_0(compiler::CodeAssemblerState* state_, TNode<JSListFormat> p_o);
void StoreJSListFormatIcuFormatter_0(compiler::CodeAssemblerState* state_, TNode<JSListFormat> p_o, TNode<Foreign> p_v);
TNode<Smi> LoadJSListFormatFlags_0(compiler::CodeAssemblerState* state_, TNode<JSListFormat> p_o);
void StoreJSListFormatFlags_0(compiler::CodeAssemblerState* state_, TNode<JSListFormat> p_o, TNode<Smi> p_v);
TNode<JSListFormat> DownCastForTorqueClass_JSListFormat_0(compiler::CodeAssemblerState* state_, TNode<HeapObject> p_o, compiler::CodeAssemblerLabel* label_CastError);
} // namespace internal
} // namespace v8
#endif // V8_GEN_TORQUE_GENERATED_SRC_OBJECTS_JS_LIST_FORMAT_TQ_CSA_H_
