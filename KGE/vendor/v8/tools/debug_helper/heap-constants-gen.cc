
#include <cstdint>
#include <string>

#include "src/common/ptr-compr-inl.h"
#include "tools/debug_helper/debug-helper-internal.h"

namespace v8 {
namespace internal {
namespace debug_helper_internal {

std::string FindKnownObjectInMapSpace(uintptr_t offset) {
  switch (offset) {
    case 8473: return "ExternalMap";
    case 8513: return "JSMessageObjectMap";
    default: return "";
  }
}

std::string FindKnownObjectInReadOnlySpace(uintptr_t offset) {
  switch (offset) {
    case 8473: return "MetaMap";
    case 8513: return "NullMap";
    case 8553: return "StrongDescriptorArrayMap";
    case 8593: return "WeakFixedArrayMap";
    case 8657: return "EnumCacheMap";
    case 8709: return "FixedArrayMap";
    case 8785: return "OneByteInternalizedStringMap";
    case 8861: return "FreeSpaceMap";
    case 8901: return "OnePointerFillerMap";
    case 8941: return "TwoPointerFillerMap";
    case 8981: return "UninitializedMap";
    case 9101: return "UndefinedMap";
    case 9169: return "HeapNumberMap";
    case 9221: return "TheHoleMap";
    case 9317: return "BooleanMap";
    case 9481: return "ByteArrayMap";
    case 9521: return "FixedCOWArrayMap";
    case 9561: return "HashTableMap";
    case 9601: return "SymbolMap";
    case 9641: return "OneByteStringMap";
    case 9681: return "ScopeInfoMap";
    case 9721: return "SharedFunctionInfoMap";
    case 9761: return "CodeMap";
    case 9801: return "CellMap";
    case 9841: return "GlobalPropertyCellMap";
    case 9881: return "ForeignMap";
    case 9921: return "TransitionArrayMap";
    case 9961: return "ThinOneByteStringMap";
    case 10001: return "FeedbackVectorMap";
    case 10057: return "ArgumentsMarkerMap";
    case 10153: return "ExceptionMap";
    case 10245: return "TerminationExceptionMap";
    case 10349: return "OptimizedOutMap";
    case 10445: return "StaleRegisterMap";
    case 10541: return "ScriptContextTableMap";
    case 10581: return "ClosureFeedbackCellArrayMap";
    case 10621: return "FeedbackMetadataArrayMap";
    case 10661: return "ArrayListMap";
    case 10701: return "BigIntMap";
    case 10741: return "ObjectBoilerplateDescriptionMap";
    case 10781: return "BytecodeArrayMap";
    case 10821: return "CodeDataContainerMap";
    case 10861: return "CoverageInfoMap";
    case 10901: return "FixedDoubleArrayMap";
    case 10941: return "GlobalDictionaryMap";
    case 10981: return "ManyClosuresCellMap";
    case 11021: return "MegaDomHandlerMap";
    case 11061: return "ModuleInfoMap";
    case 11101: return "NameDictionaryMap";
    case 11141: return "NoClosuresCellMap";
    case 11181: return "NumberDictionaryMap";
    case 11221: return "OneClosureCellMap";
    case 11261: return "OrderedHashMapMap";
    case 11301: return "OrderedHashSetMap";
    case 11341: return "OrderedNameDictionaryMap";
    case 11381: return "PreparseDataMap";
    case 11421: return "PropertyArrayMap";
    case 11461: return "SideEffectCallHandlerInfoMap";
    case 11501: return "SideEffectFreeCallHandlerInfoMap";
    case 11541: return "NextCallSideEffectFreeCallHandlerInfoMap";
    case 11581: return "SimpleNumberDictionaryMap";
    case 11621: return "SmallOrderedHashMapMap";
    case 11661: return "SmallOrderedHashSetMap";
    case 11701: return "SmallOrderedNameDictionaryMap";
    case 11741: return "SourceTextModuleMap";
    case 11781: return "SwissNameDictionaryMap";
    case 11821: return "SyntheticModuleMap";
    case 11861: return "WasmCapiFunctionDataMap";
    case 11901: return "WasmExportedFunctionDataMap";
    case 11941: return "WasmJSFunctionDataMap";
    case 11981: return "WasmTypeInfoMap";
    case 12021: return "WeakArrayListMap";
    case 12061: return "EphemeronHashTableMap";
    case 12101: return "EmbedderDataArrayMap";
    case 12141: return "WeakCellMap";
    case 12181: return "StringMap";
    case 12221: return "ConsOneByteStringMap";
    case 12261: return "ConsStringMap";
    case 12301: return "ThinStringMap";
    case 12341: return "SlicedStringMap";
    case 12381: return "SlicedOneByteStringMap";
    case 12421: return "ExternalStringMap";
    case 12461: return "ExternalOneByteStringMap";
    case 12501: return "UncachedExternalStringMap";
    case 12541: return "InternalizedStringMap";
    case 12581: return "ExternalInternalizedStringMap";
    case 12621: return "ExternalOneByteInternalizedStringMap";
    case 12661: return "UncachedExternalInternalizedStringMap";
    case 12701: return "UncachedExternalOneByteInternalizedStringMap";
    case 12741: return "UncachedExternalOneByteStringMap";
    case 12781: return "SelfReferenceMarkerMap";
    case 12821: return "BasicBlockCountersMarkerMap";
    case 12889: return "ArrayBoilerplateDescriptionMap";
    case 13145: return "InterceptorInfoMap";
    case 22133: return "PromiseFulfillReactionJobTaskMap";
    case 22173: return "PromiseRejectReactionJobTaskMap";
    case 22213: return "CallableTaskMap";
    case 22253: return "CallbackTaskMap";
    case 22293: return "PromiseResolveThenableJobTaskMap";
    case 22333: return "FunctionTemplateInfoMap";
    case 22373: return "ObjectTemplateInfoMap";
    case 22413: return "AccessCheckInfoMap";
    case 22453: return "AccessorInfoMap";
    case 22493: return "AccessorPairMap";
    case 22533: return "AliasedArgumentsEntryMap";
    case 22573: return "AllocationMementoMap";
    case 22613: return "AsmWasmDataMap";
    case 22653: return "AsyncGeneratorRequestMap";
    case 22693: return "BaselineDataMap";
    case 22733: return "BreakPointMap";
    case 22773: return "BreakPointInfoMap";
    case 22813: return "CachedTemplateObjectMap";
    case 22853: return "ClassPositionsMap";
    case 22893: return "DebugInfoMap";
    case 22933: return "FunctionTemplateRareDataMap";
    case 22973: return "InterpreterDataMap";
    case 23013: return "ModuleRequestMap";
    case 23053: return "PromiseCapabilityMap";
    case 23093: return "PromiseReactionMap";
    case 23133: return "PropertyDescriptorObjectMap";
    case 23173: return "PrototypeInfoMap";
    case 23213: return "RegExpBoilerplateDescriptionMap";
    case 23253: return "ScriptMap";
    case 23293: return "SourceTextModuleInfoEntryMap";
    case 23333: return "StackFrameInfoMap";
    case 23373: return "TemplateObjectDescriptionMap";
    case 23413: return "Tuple2Map";
    case 23453: return "WasmExceptionTagMap";
    case 23493: return "WasmIndirectFunctionTableMap";
    case 23533: return "SloppyArgumentsElementsMap";
    case 23573: return "DescriptorArrayMap";
    case 23613: return "UncompiledDataWithoutPreparseDataMap";
    case 23653: return "UncompiledDataWithPreparseDataMap";
    case 23693: return "OnHeapBasicBlockProfilerDataMap";
    case 23733: return "InternalClassMap";
    case 23773: return "SmiPairMap";
    case 23813: return "SmiBoxMap";
    case 23853: return "ExportedSubClassBaseMap";
    case 23893: return "ExportedSubClassMap";
    case 23933: return "AbstractInternalClassSubclass1Map";
    case 23973: return "AbstractInternalClassSubclass2Map";
    case 24013: return "InternalClassWithSmiElementsMap";
    case 24053: return "InternalClassWithStructElementsMap";
    case 24093: return "ExportedSubClass2Map";
    case 24133: return "SortStateMap";
    case 24173: return "AllocationSiteWithWeakNextMap";
    case 24213: return "AllocationSiteWithoutWeakNextMap";
    case 24253: return "LoadHandler1Map";
    case 24293: return "LoadHandler2Map";
    case 24333: return "LoadHandler3Map";
    case 24373: return "StoreHandler0Map";
    case 24413: return "StoreHandler1Map";
    case 24453: return "StoreHandler2Map";
    case 24493: return "StoreHandler3Map";
    case 8633: return "EmptyWeakFixedArray";
    case 8641: return "EmptyDescriptorArray";
    case 8697: return "EmptyEnumCache";
    case 8749: return "EmptyFixedArray";
    case 8757: return "NullValue";
    case 9021: return "UninitializedValue";
    case 9141: return "UndefinedValue";
    case 9209: return "NanValue";
    case 9261: return "TheHoleValue";
    case 9305: return "HoleNanValue";
    case 9357: return "TrueValue";
    case 9421: return "FalseValue";
    case 9469: return "empty_string";
    case 10041: return "EmptyScopeInfo";
    case 10097: return "ArgumentsMarker";
    case 10193: return "Exception";
    case 10285: return "TerminationException";
    case 10389: return "OptimizedOut";
    case 10485: return "StaleRegister";
    case 12861: return "EmptyPropertyArray";
    case 12869: return "EmptyByteArray";
    case 12877: return "EmptyObjectBoilerplateDescription";
    case 12929: return "EmptyArrayBoilerplateDescription";
    case 12941: return "EmptyClosureFeedbackCellArray";
    case 12949: return "EmptySlowElementDictionary";
    case 12985: return "EmptyOrderedHashMap";
    case 13005: return "EmptyOrderedHashSet";
    case 13025: return "EmptyFeedbackMetadata";
    case 13037: return "EmptyPropertyDictionary";
    case 13077: return "EmptyOrderedPropertyDictionary";
    case 13101: return "EmptySwissPropertyDictionary";
    case 13185: return "NoOpInterceptorInfo";
    case 13225: return "EmptyWeakArrayList";
    case 13237: return "InfinityValue";
    case 13249: return "MinusZeroValue";
    case 13261: return "MinusInfinityValue";
    case 13273: return "SelfReferenceMarker";
    case 13337: return "BasicBlockCountersMarker";
    case 13405: return "OffHeapTrampolineRelocationInfo";
    case 13417: return "TrampolineTrivialCodeDataContainer";
    case 13429: return "TrampolinePromiseRejectionCodeDataContainer";
    case 13441: return "GlobalThisBindingScopeInfo";
    case 13493: return "EmptyFunctionScopeInfo";
    case 13529: return "NativeScopeInfo";
    case 13553: return "HashSeed";
    default: return "";
  }
}

std::string FindKnownObjectInOldSpace(uintptr_t offset) {
  switch (offset) {
    case 8473: return "ArgumentsIteratorAccessor";
    case 8541: return "ArrayLengthAccessor";
    case 8609: return "BoundFunctionLengthAccessor";
    case 8677: return "BoundFunctionNameAccessor";
    case 8745: return "ErrorStackAccessor";
    case 8813: return "FunctionArgumentsAccessor";
    case 8881: return "FunctionCallerAccessor";
    case 8949: return "FunctionNameAccessor";
    case 9017: return "FunctionLengthAccessor";
    case 9085: return "FunctionPrototypeAccessor";
    case 9153: return "StringLengthAccessor";
    case 9221: return "InvalidPrototypeValidityCell";
    case 9229: return "EmptyScript";
    case 9293: return "ManyClosuresCell";
    case 9305: return "ArrayConstructorProtector";
    case 9325: return "NoElementsProtector";
    case 9345: return "MegaDOMProtector";
    case 9365: return "IsConcatSpreadableProtector";
    case 9385: return "ArraySpeciesProtector";
    case 9405: return "TypedArraySpeciesProtector";
    case 9425: return "PromiseSpeciesProtector";
    case 9445: return "RegExpSpeciesProtector";
    case 9465: return "StringLengthProtector";
    case 9485: return "ArrayIteratorProtector";
    case 9505: return "ArrayBufferDetachingProtector";
    case 9525: return "PromiseHookProtector";
    case 9545: return "PromiseResolveProtector";
    case 9565: return "MapIteratorProtector";
    case 9585: return "PromiseThenProtector";
    case 9605: return "SetIteratorProtector";
    case 9625: return "StringIteratorProtector";
    case 9645: return "SingleCharacterStringCache";
    case 10677: return "StringSplitCache";
    case 11709: return "RegExpMultipleCache";
    case 12741: return "BuiltinsConstantsTable";
    case 13781: return "AsyncFunctionAwaitRejectSharedFun";
    case 13817: return "AsyncFunctionAwaitResolveSharedFun";
    case 13853: return "AsyncGeneratorAwaitRejectSharedFun";
    case 13889: return "AsyncGeneratorAwaitResolveSharedFun";
    case 13925: return "AsyncGeneratorYieldResolveSharedFun";
    case 13961: return "AsyncGeneratorReturnResolveSharedFun";
    case 13997: return "AsyncGeneratorReturnClosedRejectSharedFun";
    case 14033: return "AsyncGeneratorReturnClosedResolveSharedFun";
    case 14069: return "AsyncIteratorValueUnwrapSharedFun";
    case 14105: return "PromiseAllResolveElementSharedFun";
    case 14141: return "PromiseAllSettledResolveElementSharedFun";
    case 14177: return "PromiseAllSettledRejectElementSharedFun";
    case 14213: return "PromiseAnyRejectElementSharedFun";
    case 14249: return "PromiseCapabilityDefaultRejectSharedFun";
    case 14285: return "PromiseCapabilityDefaultResolveSharedFun";
    case 14321: return "PromiseCatchFinallySharedFun";
    case 14357: return "PromiseGetCapabilitiesExecutorSharedFun";
    case 14393: return "PromiseThenFinallySharedFun";
    case 14429: return "PromiseThrowerFinallySharedFun";
    case 14465: return "PromiseValueThunkFinallySharedFun";
    case 14501: return "ProxyRevokeSharedFun";
    default: return "";
  }
}

int FindKnownMapInstanceTypeInMapSpace(uintptr_t offset) {
  switch (offset) {
    case 8473: return 1057;
    case 8513: return 1098;
    default: return -1;
  }
}

int FindKnownMapInstanceTypeInReadOnlySpace(uintptr_t offset) {
  switch (offset) {
    case 8473: return 172;
    case 8513: return 67;
    case 8553: return 154;
    case 8593: return 159;
    case 8657: return 101;
    case 8709: return 119;
    case 8785: return 8;
    case 8861: return 169;
    case 8901: return 168;
    case 8941: return 168;
    case 8981: return 67;
    case 9101: return 67;
    case 9169: return 66;
    case 9221: return 67;
    case 9317: return 67;
    case 9481: return 132;
    case 9521: return 119;
    case 9561: return 120;
    case 9601: return 64;
    case 9641: return 40;
    case 9681: return 178;
    case 9721: return 179;
    case 9761: return 162;
    case 9801: return 161;
    case 9841: return 177;
    case 9881: return 70;
    case 9921: return 160;
    case 9961: return 45;
    case 10001: return 167;
    case 10057: return 67;
    case 10153: return 67;
    case 10245: return 67;
    case 10349: return 67;
    case 10445: return 67;
    case 10541: return 131;
    case 10581: return 129;
    case 10621: return 166;
    case 10661: return 119;
    case 10701: return 65;
    case 10741: return 130;
    case 10781: return 133;
    case 10821: return 163;
    case 10861: return 164;
    case 10901: return 134;
    case 10941: return 122;
    case 10981: return 102;
    case 11021: return 173;
    case 11061: return 119;
    case 11101: return 123;
    case 11141: return 102;
    case 11181: return 124;
    case 11221: return 102;
    case 11261: return 125;
    case 11301: return 126;
    case 11341: return 127;
    case 11381: return 175;
    case 11421: return 176;
    case 11461: return 98;
    case 11501: return 98;
    case 11541: return 98;
    case 11581: return 128;
    case 11621: return 150;
    case 11661: return 151;
    case 11701: return 152;
    case 11741: return 155;
    case 11781: return 183;
    case 11821: return 156;
    case 11861: return 72;
    case 11901: return 73;
    case 11941: return 74;
    case 11981: return 75;
    case 12021: return 184;
    case 12061: return 121;
    case 12101: return 165;
    case 12141: return 185;
    case 12181: return 32;
    case 12221: return 41;
    case 12261: return 33;
    case 12301: return 37;
    case 12341: return 35;
    case 12381: return 43;
    case 12421: return 34;
    case 12461: return 42;
    case 12501: return 50;
    case 12541: return 0;
    case 12581: return 2;
    case 12621: return 10;
    case 12661: return 18;
    case 12701: return 26;
    case 12741: return 58;
    case 12781: return 67;
    case 12821: return 67;
    case 12889: return 91;
    case 13145: return 104;
    case 22133: return 76;
    case 22173: return 77;
    case 22213: return 78;
    case 22253: return 79;
    case 22293: return 80;
    case 22333: return 83;
    case 22373: return 84;
    case 22413: return 85;
    case 22453: return 86;
    case 22493: return 87;
    case 22533: return 88;
    case 22573: return 89;
    case 22613: return 92;
    case 22653: return 93;
    case 22693: return 94;
    case 22733: return 95;
    case 22773: return 96;
    case 22813: return 97;
    case 22853: return 99;
    case 22893: return 100;
    case 22933: return 103;
    case 22973: return 105;
    case 23013: return 106;
    case 23053: return 107;
    case 23093: return 108;
    case 23133: return 109;
    case 23173: return 110;
    case 23213: return 111;
    case 23253: return 112;
    case 23293: return 113;
    case 23333: return 114;
    case 23373: return 115;
    case 23413: return 116;
    case 23453: return 117;
    case 23493: return 118;
    case 23533: return 136;
    case 23573: return 153;
    case 23613: return 158;
    case 23653: return 157;
    case 23693: return 174;
    case 23733: return 170;
    case 23773: return 181;
    case 23813: return 180;
    case 23853: return 147;
    case 23893: return 148;
    case 23933: return 68;
    case 23973: return 69;
    case 24013: return 135;
    case 24053: return 171;
    case 24093: return 149;
    case 24133: return 182;
    case 24173: return 90;
    case 24213: return 90;
    case 24253: return 81;
    case 24293: return 81;
    case 24333: return 81;
    case 24373: return 82;
    case 24413: return 82;
    case 24453: return 82;
    case 24493: return 82;
    default: return -1;
  }
}

void FillInUnknownHeapAddresses(d::HeapAddresses* heap_addresses, uintptr_t any_uncompressed_ptr) {
  if (heap_addresses->any_heap_pointer == 0) {
    heap_addresses->any_heap_pointer = any_uncompressed_ptr;
  }
  if (heap_addresses->old_space_first_page == 0) {
    heap_addresses->old_space_first_page = i::DecompressTaggedPointer(any_uncompressed_ptr, 135004160);
  }
  if (heap_addresses->map_space_first_page == 0) {
    heap_addresses->map_space_first_page = i::DecompressTaggedPointer(any_uncompressed_ptr, 135266304);
  }
  if (heap_addresses->read_only_space_first_page == 0) {
    heap_addresses->read_only_space_first_page = i::DecompressTaggedPointer(any_uncompressed_ptr, 134217728);
  }
}

}
}
}
