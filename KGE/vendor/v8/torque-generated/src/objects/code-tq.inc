class BytecodeArray;
class CodeDataContainer;
// Alias for HeapObject::IsBytecodeArray() that avoids inlining.
V8_EXPORT_PRIVATE bool IsBytecodeArray_NonInline(HeapObject o);
template <class D, class P>
class TorqueGeneratedBytecodeArray : public P {
  static_assert(std::is_same<BytecodeArray, D>::value,
    "Use this class as direct base for BytecodeArray.");
  static_assert(std::is_same<FixedArrayBase, P>::value,
    "Pass in FixedArrayBase as second template parameter for TorqueGeneratedBytecodeArray.");
 public: 
  using Super = P;
  using TorqueGeneratedClass = TorqueGeneratedBytecodeArray<D,P>;

inline FixedArray constant_pool() const;
inline FixedArray constant_pool(PtrComprCageBase cage_base) const;
inline void set_constant_pool(FixedArray value, WriteBarrierMode mode = UPDATE_WRITE_BARRIER);

inline ByteArray handler_table() const;
inline ByteArray handler_table(PtrComprCageBase cage_base) const;
inline void set_handler_table(ByteArray value, WriteBarrierMode mode = UPDATE_WRITE_BARRIER);

  // Torque type: (Undefined | class ByteArray | Exception)
inline HeapObject source_position_table(AcquireLoadTag) const;
inline HeapObject source_position_table(PtrComprCageBase cage_base, AcquireLoadTag) const;
inline void set_source_position_table(HeapObject value, ReleaseStoreTag, WriteBarrierMode mode = UPDATE_WRITE_BARRIER);

inline int32_t frame_size() const;
inline void set_frame_size(int32_t value);

inline int32_t parameter_size() const;
inline void set_parameter_size(int32_t value);

inline int32_t incoming_new_target_or_generator_register() const;
inline void set_incoming_new_target_or_generator_register(int32_t value);

inline int8_t osr_loop_nesting_level() const;
inline void set_osr_loop_nesting_level(int8_t value);

inline int8_t bytecode_age() const;
inline void set_bytecode_age(int8_t value);

V8_INLINE static D cast(Object object) {
  return D(object.ptr());
}

V8_INLINE static D unchecked_cast(Object object) {
  return bit_cast<D>(object);
}

#ifdef VERIFY_HEAP
V8_EXPORT_PRIVATE void BytecodeArrayVerify(Isolate* isolate);
#endif  // VERIFY_HEAP

  static constexpr int kStartOfStrongFieldsOffset = P::kHeaderSize;
  static constexpr int kConstantPoolOffset = P::kHeaderSize;
  static constexpr int kConstantPoolOffsetEnd = kConstantPoolOffset + kTaggedSize - 1;
  static constexpr int kHandlerTableOffset = kConstantPoolOffsetEnd + 1;
  static constexpr int kHandlerTableOffsetEnd = kHandlerTableOffset + kTaggedSize - 1;
  static constexpr int kSourcePositionTableOffset = kHandlerTableOffsetEnd + 1;
  static constexpr int kSourcePositionTableOffsetEnd = kSourcePositionTableOffset + kTaggedSize - 1;
  static constexpr int kEndOfStrongFieldsOffset = kSourcePositionTableOffsetEnd + 1;
  static constexpr int kFrameSizeOffset = kSourcePositionTableOffsetEnd + 1;
  static constexpr int kFrameSizeOffsetEnd = kFrameSizeOffset + kInt32Size - 1;
  static constexpr int kParameterSizeOffset = kFrameSizeOffsetEnd + 1;
  static constexpr int kParameterSizeOffsetEnd = kParameterSizeOffset + kInt32Size - 1;
  static constexpr int kIncomingNewTargetOrGeneratorRegisterOffset = kParameterSizeOffsetEnd + 1;
  static constexpr int kIncomingNewTargetOrGeneratorRegisterOffsetEnd = kIncomingNewTargetOrGeneratorRegisterOffset + kInt32Size - 1;
  static constexpr int kOsrLoopNestingLevelOffset = kIncomingNewTargetOrGeneratorRegisterOffsetEnd + 1;
  static constexpr int kOsrLoopNestingLevelOffsetEnd = kOsrLoopNestingLevelOffset + kUInt8Size - 1;
  static constexpr int kBytecodeAgeOffset = kOsrLoopNestingLevelOffsetEnd + 1;
  static constexpr int kBytecodeAgeOffsetEnd = kBytecodeAgeOffset + kUInt8Size - 1;
  static constexpr int kStartOfWeakFieldsOffset = kBytecodeAgeOffsetEnd + 1;
  static constexpr int kEndOfWeakFieldsOffset = kBytecodeAgeOffsetEnd + 1;
  static constexpr int kHeaderSize = kBytecodeAgeOffsetEnd + 1;
  static constexpr int kSize = kBytecodeAgeOffsetEnd + 1;

V8_INLINE static constexpr int32_t SizeFor() {
    DCHECK(kHeaderSize == kSize && kHeaderSize == 34);
    int32_t size = kHeaderSize;
    size = OBJECT_POINTER_ALIGN(size);
    return size;
}

V8_INLINE int32_t AllocatedSize() const {
    return SizeFor();
}

  friend class Factory;

 public:
  template <class DAlias = D>
  constexpr TorqueGeneratedBytecodeArray() : P() {
    static_assert(std::is_base_of<TorqueGeneratedBytecodeArray, 
      DAlias>::value,
      "class TorqueGeneratedBytecodeArray should be used as direct base for BytecodeArray.");
  }
 protected:
  inline explicit TorqueGeneratedBytecodeArray(Address ptr);
  // Special-purpose constructor for subclasses that have fast paths where
  // their ptr() is a Smi.
  inline explicit TorqueGeneratedBytecodeArray(Address ptr, HeapObject::AllowInlineSmiStorage allow_smi);
};

