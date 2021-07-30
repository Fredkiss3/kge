#ifndef V8_GEN_TORQUE_GENERATED_SRC_OBJECTS_JS_BREAK_ITERATOR_TQ_CSA_H_
#define V8_GEN_TORQUE_GENERATED_SRC_OBJECTS_JS_BREAK_ITERATOR_TQ_CSA_H_
#include "src/builtins/torque-csa-header-includes.h"

namespace v8 {
namespace internal {
TNode<JSV8BreakIterator> Cast_JSV8BreakIterator_0(compiler::CodeAssemblerState* state_, TNode<HeapObject> p_obj, compiler::CodeAssemblerLabel* label_CastError);
TNode<String> LoadJSV8BreakIteratorLocale_0(compiler::CodeAssemblerState* state_, TNode<JSV8BreakIterator> p_o);
void StoreJSV8BreakIteratorLocale_0(compiler::CodeAssemblerState* state_, TNode<JSV8BreakIterator> p_o, TNode<String> p_v);
TNode<Foreign> LoadJSV8BreakIteratorBreakIterator_0(compiler::CodeAssemblerState* state_, TNode<JSV8BreakIterator> p_o);
void StoreJSV8BreakIteratorBreakIterator_0(compiler::CodeAssemblerState* state_, TNode<JSV8BreakIterator> p_o, TNode<Foreign> p_v);
TNode<Foreign> LoadJSV8BreakIteratorUnicodeString_0(compiler::CodeAssemblerState* state_, TNode<JSV8BreakIterator> p_o);
void StoreJSV8BreakIteratorUnicodeString_0(compiler::CodeAssemblerState* state_, TNode<JSV8BreakIterator> p_o, TNode<Foreign> p_v);
TNode<HeapObject> LoadJSV8BreakIteratorBoundAdoptText_0(compiler::CodeAssemblerState* state_, TNode<JSV8BreakIterator> p_o);
void StoreJSV8BreakIteratorBoundAdoptText_0(compiler::CodeAssemblerState* state_, TNode<JSV8BreakIterator> p_o, TNode<HeapObject> p_v);
TNode<HeapObject> LoadJSV8BreakIteratorBoundFirst_0(compiler::CodeAssemblerState* state_, TNode<JSV8BreakIterator> p_o);
void StoreJSV8BreakIteratorBoundFirst_0(compiler::CodeAssemblerState* state_, TNode<JSV8BreakIterator> p_o, TNode<HeapObject> p_v);
TNode<HeapObject> LoadJSV8BreakIteratorBoundNext_0(compiler::CodeAssemblerState* state_, TNode<JSV8BreakIterator> p_o);
void StoreJSV8BreakIteratorBoundNext_0(compiler::CodeAssemblerState* state_, TNode<JSV8BreakIterator> p_o, TNode<HeapObject> p_v);
TNode<HeapObject> LoadJSV8BreakIteratorBoundCurrent_0(compiler::CodeAssemblerState* state_, TNode<JSV8BreakIterator> p_o);
void StoreJSV8BreakIteratorBoundCurrent_0(compiler::CodeAssemblerState* state_, TNode<JSV8BreakIterator> p_o, TNode<HeapObject> p_v);
TNode<HeapObject> LoadJSV8BreakIteratorBoundBreakType_0(compiler::CodeAssemblerState* state_, TNode<JSV8BreakIterator> p_o);
void StoreJSV8BreakIteratorBoundBreakType_0(compiler::CodeAssemblerState* state_, TNode<JSV8BreakIterator> p_o, TNode<HeapObject> p_v);
TNode<JSV8BreakIterator> DownCastForTorqueClass_JSV8BreakIterator_0(compiler::CodeAssemblerState* state_, TNode<HeapObject> p_o, compiler::CodeAssemblerLabel* label_CastError);
} // namespace internal
} // namespace v8
#endif // V8_GEN_TORQUE_GENERATED_SRC_OBJECTS_JS_BREAK_ITERATOR_TQ_CSA_H_
