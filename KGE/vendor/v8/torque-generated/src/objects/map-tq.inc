class Map;
// Alias for HeapObject::IsMap() that avoids inlining.
V8_EXPORT_PRIVATE bool IsMap_NonInline(HeapObject o);
template <class D, class P>
class TorqueGeneratedMap : public P {
  static_assert(std::is_same<Map, D>::value,
    "Use this class as direct base for Map.");
  static_assert(std::is_same<HeapObject, P>::value,
    "Pass in HeapObject as second template parameter for TorqueGeneratedMap.");
 public: 
  using Super = P;
  using TorqueGeneratedClass = TorqueGeneratedMap<D,P>;

inline uint8_t instance_size_in_words() const;
inline void set_instance_size_in_words(uint8_t value);

inline uint8_t inobject_properties_start_or_constructor_function_index() const;
inline void set_inobject_properties_start_or_constructor_function_index(uint8_t value);

inline uint8_t used_or_unused_instance_size_in_words() const;
inline void set_used_or_unused_instance_size_in_words(uint8_t value);

inline uint8_t visitor_id() const;
inline void set_visitor_id(uint8_t value);

inline InstanceType instance_type() const;
inline void set_instance_type(InstanceType value);

inline uint8_t bit_field() const;
inline void set_bit_field(uint8_t value);

inline uint8_t bit_field2() const;
inline void set_bit_field2(uint8_t value);

inline uint32_t bit_field3() const;
inline void set_bit_field3(uint32_t value);

  // Torque type: (class JSReceiver | Null)
inline HeapObject prototype() const;
inline HeapObject prototype(PtrComprCageBase cage_base) const;
inline void set_prototype(HeapObject value, WriteBarrierMode mode = UPDATE_WRITE_BARRIER);

inline Object constructor_or_back_pointer_or_native_context() const;
inline Object constructor_or_back_pointer_or_native_context(PtrComprCageBase cage_base) const;
inline void set_constructor_or_back_pointer_or_native_context(Object value, WriteBarrierMode mode = UPDATE_WRITE_BARRIER);

inline DescriptorArray instance_descriptors() const;
inline DescriptorArray instance_descriptors(PtrComprCageBase cage_base) const;
inline void set_instance_descriptors(DescriptorArray value, WriteBarrierMode mode = UPDATE_WRITE_BARRIER);

  // Torque type: DependentCode
inline WeakFixedArray dependent_code() const;
inline WeakFixedArray dependent_code(PtrComprCageBase cage_base) const;
inline void set_dependent_code(WeakFixedArray value, WriteBarrierMode mode = UPDATE_WRITE_BARRIER);

  // Torque type: (Smi | class Cell)
inline Object prototype_validity_cell() const;
inline Object prototype_validity_cell(PtrComprCageBase cage_base) const;
inline void set_prototype_validity_cell(Object value, WriteBarrierMode mode = UPDATE_WRITE_BARRIER);

  // Torque type: (Smi | class TransitionArray | class Map | Weak<class Map> | class PrototypeInfo)
inline MaybeObject transitions_or_prototype_info() const;
inline MaybeObject transitions_or_prototype_info(PtrComprCageBase cage_base) const;
inline void set_transitions_or_prototype_info(MaybeObject value, WriteBarrierMode mode = UPDATE_WRITE_BARRIER);

V8_INLINE static D cast(Object object) {
  return D(object.ptr());
}

V8_INLINE static D unchecked_cast(Object object) {
  return bit_cast<D>(object);
}

#ifdef VERIFY_HEAP
V8_EXPORT_PRIVATE void MapVerify(Isolate* isolate);
#endif  // VERIFY_HEAP

  static constexpr int kInstanceSizeInWordsOffset = P::kHeaderSize;
  static constexpr int kInstanceSizeInWordsOffsetEnd = kInstanceSizeInWordsOffset + kUInt8Size - 1;
  static constexpr int kInobjectPropertiesStartOrConstructorFunctionIndexOffset = kInstanceSizeInWordsOffsetEnd + 1;
  static constexpr int kInobjectPropertiesStartOrConstructorFunctionIndexOffsetEnd = kInobjectPropertiesStartOrConstructorFunctionIndexOffset + kUInt8Size - 1;
  static constexpr int kUsedOrUnusedInstanceSizeInWordsOffset = kInobjectPropertiesStartOrConstructorFunctionIndexOffsetEnd + 1;
  static constexpr int kUsedOrUnusedInstanceSizeInWordsOffsetEnd = kUsedOrUnusedInstanceSizeInWordsOffset + kUInt8Size - 1;
  static constexpr int kVisitorIdOffset = kUsedOrUnusedInstanceSizeInWordsOffsetEnd + 1;
  static constexpr int kVisitorIdOffsetEnd = kVisitorIdOffset + kUInt8Size - 1;
  static constexpr int kInstanceTypeOffset = kVisitorIdOffsetEnd + 1;
  static constexpr int kInstanceTypeOffsetEnd = kInstanceTypeOffset + kUInt16Size - 1;
  static constexpr int kBitFieldOffset = kInstanceTypeOffsetEnd + 1;
  static constexpr int kBitFieldOffsetEnd = kBitFieldOffset + kUInt8Size - 1;
  static constexpr int kBitField2Offset = kBitFieldOffsetEnd + 1;
  static constexpr int kBitField2OffsetEnd = kBitField2Offset + kUInt8Size - 1;
  static constexpr int kBitField3Offset = kBitField2OffsetEnd + 1;
  static constexpr int kBitField3OffsetEnd = kBitField3Offset + kInt32Size - 1;
  static constexpr int kOptionalPaddingOffset = kBitField3OffsetEnd + 1;
  static constexpr int kOptionalPaddingOffsetEnd = kOptionalPaddingOffset + 0 - 1;
  static constexpr int kStartOfStrongFieldsOffset = kOptionalPaddingOffsetEnd + 1;
  static constexpr int kPrototypeOffset = kOptionalPaddingOffsetEnd + 1;
  static constexpr int kPrototypeOffsetEnd = kPrototypeOffset + kTaggedSize - 1;
  static constexpr int kConstructorOrBackPointerOrNativeContextOffset = kPrototypeOffsetEnd + 1;
  static constexpr int kConstructorOrBackPointerOrNativeContextOffsetEnd = kConstructorOrBackPointerOrNativeContextOffset + kTaggedSize - 1;
  static constexpr int kInstanceDescriptorsOffset = kConstructorOrBackPointerOrNativeContextOffsetEnd + 1;
  static constexpr int kInstanceDescriptorsOffsetEnd = kInstanceDescriptorsOffset + kTaggedSize - 1;
  static constexpr int kDependentCodeOffset = kInstanceDescriptorsOffsetEnd + 1;
  static constexpr int kDependentCodeOffsetEnd = kDependentCodeOffset + kTaggedSize - 1;
  static constexpr int kPrototypeValidityCellOffset = kDependentCodeOffsetEnd + 1;
  static constexpr int kPrototypeValidityCellOffsetEnd = kPrototypeValidityCellOffset + kTaggedSize - 1;
  static constexpr int kEndOfStrongFieldsOffset = kPrototypeValidityCellOffsetEnd + 1;
  static constexpr int kStartOfWeakFieldsOffset = kPrototypeValidityCellOffsetEnd + 1;
  static constexpr int kTransitionsOrPrototypeInfoOffset = kPrototypeValidityCellOffsetEnd + 1;
  static constexpr int kTransitionsOrPrototypeInfoOffsetEnd = kTransitionsOrPrototypeInfoOffset + kTaggedSize - 1;
  static constexpr int kEndOfWeakFieldsOffset = kTransitionsOrPrototypeInfoOffsetEnd + 1;
  static constexpr int kHeaderSize = kTransitionsOrPrototypeInfoOffsetEnd + 1;
  static constexpr int kSize = kTransitionsOrPrototypeInfoOffsetEnd + 1;

V8_INLINE static constexpr int32_t SizeFor() {
    DCHECK(kHeaderSize == kSize && kHeaderSize == 40);
    int32_t size = kHeaderSize;
    return size;
}

V8_INLINE int32_t AllocatedSize() const {
    return SizeFor();
}

  friend class Factory;

 public:
  template <class DAlias = D>
  constexpr TorqueGeneratedMap() : P() {
    static_assert(std::is_base_of<TorqueGeneratedMap, 
      DAlias>::value,
      "class TorqueGeneratedMap should be used as direct base for Map.");
  }
 protected:
  inline explicit TorqueGeneratedMap(Address ptr);
  // Special-purpose constructor for subclasses that have fast paths where
  // their ptr() is a Smi.
  inline explicit TorqueGeneratedMap(Address ptr, HeapObject::AllowInlineSmiStorage allow_smi);
};

