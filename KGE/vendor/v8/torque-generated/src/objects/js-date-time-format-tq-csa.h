#ifndef V8_GEN_TORQUE_GENERATED_SRC_OBJECTS_JS_DATE_TIME_FORMAT_TQ_CSA_H_
#define V8_GEN_TORQUE_GENERATED_SRC_OBJECTS_JS_DATE_TIME_FORMAT_TQ_CSA_H_
#include "src/builtins/torque-csa-header-includes.h"

namespace v8 {
namespace internal {
TNode<JSDateTimeFormat> Cast_JSDateTimeFormat_0(compiler::CodeAssemblerState* state_, TNode<HeapObject> p_obj, compiler::CodeAssemblerLabel* label_CastError);
TNode<String> LoadJSDateTimeFormatLocale_0(compiler::CodeAssemblerState* state_, TNode<JSDateTimeFormat> p_o);
void StoreJSDateTimeFormatLocale_0(compiler::CodeAssemblerState* state_, TNode<JSDateTimeFormat> p_o, TNode<String> p_v);
TNode<Foreign> LoadJSDateTimeFormatIcuLocale_0(compiler::CodeAssemblerState* state_, TNode<JSDateTimeFormat> p_o);
void StoreJSDateTimeFormatIcuLocale_0(compiler::CodeAssemblerState* state_, TNode<JSDateTimeFormat> p_o, TNode<Foreign> p_v);
TNode<Foreign> LoadJSDateTimeFormatIcuSimpleDateFormat_0(compiler::CodeAssemblerState* state_, TNode<JSDateTimeFormat> p_o);
void StoreJSDateTimeFormatIcuSimpleDateFormat_0(compiler::CodeAssemblerState* state_, TNode<JSDateTimeFormat> p_o, TNode<Foreign> p_v);
TNode<Foreign> LoadJSDateTimeFormatIcuDateIntervalFormat_0(compiler::CodeAssemblerState* state_, TNode<JSDateTimeFormat> p_o);
void StoreJSDateTimeFormatIcuDateIntervalFormat_0(compiler::CodeAssemblerState* state_, TNode<JSDateTimeFormat> p_o, TNode<Foreign> p_v);
TNode<HeapObject> LoadJSDateTimeFormatBoundFormat_0(compiler::CodeAssemblerState* state_, TNode<JSDateTimeFormat> p_o);
void StoreJSDateTimeFormatBoundFormat_0(compiler::CodeAssemblerState* state_, TNode<JSDateTimeFormat> p_o, TNode<HeapObject> p_v);
TNode<Smi> LoadJSDateTimeFormatFlags_0(compiler::CodeAssemblerState* state_, TNode<JSDateTimeFormat> p_o);
void StoreJSDateTimeFormatFlags_0(compiler::CodeAssemblerState* state_, TNode<JSDateTimeFormat> p_o, TNode<Smi> p_v);
TNode<JSDateTimeFormat> DownCastForTorqueClass_JSDateTimeFormat_0(compiler::CodeAssemblerState* state_, TNode<HeapObject> p_o, compiler::CodeAssemblerLabel* label_CastError);
} // namespace internal
} // namespace v8
#endif // V8_GEN_TORQUE_GENERATED_SRC_OBJECTS_JS_DATE_TIME_FORMAT_TQ_CSA_H_
