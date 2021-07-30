#include "src/objects/property-array-inl.h"

#include "torque-generated/class-verifiers.h"
#include "src/objects/instance-type-inl.h"

namespace v8 {
namespace internal {
bool IsPropertyArray_NonInline(HeapObject o) {
  return o.IsPropertyArray();}

#ifdef VERIFY_HEAP

template <>
void TorqueGeneratedPropertyArray<PropertyArray, HeapObject>::PropertyArrayVerify(Isolate* isolate) {
  TorqueGeneratedClassVerifiers::PropertyArrayVerify(PropertyArray::cast(*this), isolate);
}
#endif  // VERIFY_HEAP
} // namespace internal
} // namespace v8
