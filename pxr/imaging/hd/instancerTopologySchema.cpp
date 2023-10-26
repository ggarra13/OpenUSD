//
// Copyright 2023 Pixar
//
// Licensed under the Apache License, Version 2.0 (the "Apache License")
// with the following modification; you may not use this file except in
// compliance with the Apache License and the following modification to it:
// Section 6. Trademarks. is deleted and replaced with:
//
// 6. Trademarks. This License does not grant permission to use the trade
//    names, trademarks, service marks, or product names of the Licensor
//    and its affiliates, except as required to comply with Section 4(c) of
//    the License and to reproduce the content of the NOTICE file.
//
// You may obtain a copy of the Apache License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the Apache License with the above modification is
// distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
// KIND, either express or implied. See the Apache License for the specific
// language governing permissions and limitations under the Apache License.
//
////////////////////////////////////////////////////////////////////////

/* ************************************************************************** */
/* ** This file is generated by a script.  Do not edit directly.  Edit     ** */
/* ** defs.py or the (*)Schema.template.cpp files to make changes.         ** */
/* ************************************************************************** */

#include "pxr/imaging/hd/instancerTopologySchema.h"
#include "pxr/imaging/hd/retainedDataSource.h"

#include "pxr/base/trace/trace.h"


PXR_NAMESPACE_OPEN_SCOPE

TF_DEFINE_PUBLIC_TOKENS(HdInstancerTopologySchemaTokens,
    HDINSTANCERTOPOLOGY_SCHEMA_TOKENS);



VtArray<int>
HdInstancerTopologySchema::ComputeInstanceIndicesForProto(SdfPath const &path)
{
    TRACE_FUNCTION();

    VtArray<int> result;
    VtArray<int> matchingPrototypes;

    // If we can't get the instance indices datasource, not much point...
    HdIntArrayVectorSchema indicesSchema = GetInstanceIndices();
    if (!indicesSchema) {
        return result;
    }

    // Map from path -> matchingPrototypes.
    VtArray<SdfPath> prototypes;
    if (HdPathArrayDataSourceHandle protoDs = GetPrototypes()) {
        prototypes = protoDs->GetTypedValue(0);
    }

    for (size_t i = 0; i < prototypes.size(); ++i) {
        if (path.HasPrefix(prototypes.AsConst()[i])) {
            matchingPrototypes.push_back(int(i));
        }
    }

    VtArray<bool> mask;
    if (HdBoolArrayDataSourceHandle maskDs = GetMask()) {
        mask = maskDs->GetTypedValue(0);
    }

    // Map from matchingPrototypes -> instanceIndices, taking mask into account.
    for (int protoIndex : matchingPrototypes) {
        VtArray<int> instanceIndices;
        if (HdIntArrayDataSourceHandle indicesDs =
                indicesSchema.GetElement(protoIndex)) {
            instanceIndices = indicesDs->GetTypedValue(0);
        }

        // If mask is empty, we can just copy or append the array...
        if (mask.empty() && result.empty()) {
            result = instanceIndices;
        } else if (mask.empty()) {
            size_t oldSize = result.size();
            size_t iiSize = instanceIndices.size();
            // Note: we call result.data() here to break buffer sharing.
            result.data();
            result.resize(oldSize + iiSize);
            for (size_t i = 0; i < iiSize; ++i) {
                result[oldSize + i] = instanceIndices[i];
            }
        } else {
            for (int instanceIndex : instanceIndices) {
                if (instanceIndex >= static_cast<int>(mask.size()) ||
                        mask[instanceIndex]) {
                    result.push_back(instanceIndex);
                }
            }
        }
    }
    return result;
}


HdPathArrayDataSourceHandle
HdInstancerTopologySchema::GetPrototypes()
{
    return _GetTypedDataSource<HdPathArrayDataSource>(
        HdInstancerTopologySchemaTokens->prototypes);
}

HdIntArrayVectorSchema
HdInstancerTopologySchema::GetInstanceIndices()
{
    return HdIntArrayVectorSchema(_GetTypedDataSource<HdVectorDataSource>(
        HdInstancerTopologySchemaTokens->instanceIndices));
}

HdBoolArrayDataSourceHandle
HdInstancerTopologySchema::GetMask()
{
    return _GetTypedDataSource<HdBoolArrayDataSource>(
        HdInstancerTopologySchemaTokens->mask);
}

HdPathArrayDataSourceHandle
HdInstancerTopologySchema::GetInstanceLocations()
{
    return _GetTypedDataSource<HdPathArrayDataSource>(
        HdInstancerTopologySchemaTokens->instanceLocations);
}

/*static*/
HdContainerDataSourceHandle
HdInstancerTopologySchema::BuildRetained(
        const HdPathArrayDataSourceHandle &prototypes,
        const HdVectorDataSourceHandle &instanceIndices,
        const HdBoolArrayDataSourceHandle &mask,
        const HdPathArrayDataSourceHandle &instanceLocations
)
{
    TfToken names[4];
    HdDataSourceBaseHandle values[4];

    size_t count = 0;
    if (prototypes) {
        names[count] = HdInstancerTopologySchemaTokens->prototypes;
        values[count++] = prototypes;
    }

    if (instanceIndices) {
        names[count] = HdInstancerTopologySchemaTokens->instanceIndices;
        values[count++] = instanceIndices;
    }

    if (mask) {
        names[count] = HdInstancerTopologySchemaTokens->mask;
        values[count++] = mask;
    }

    if (instanceLocations) {
        names[count] = HdInstancerTopologySchemaTokens->instanceLocations;
        values[count++] = instanceLocations;
    }

    return HdRetainedContainerDataSource::New(count, names, values);
}

/*static*/
HdInstancerTopologySchema
HdInstancerTopologySchema::GetFromParent(
        const HdContainerDataSourceHandle &fromParentContainer)
{
    return HdInstancerTopologySchema(
        fromParentContainer
        ? HdContainerDataSource::Cast(fromParentContainer->Get(
                HdInstancerTopologySchemaTokens->instancerTopology))
        : nullptr);
}

/*static*/
const TfToken &
HdInstancerTopologySchema::GetSchemaToken()
{
    return HdInstancerTopologySchemaTokens->instancerTopology;
} 
/*static*/
const HdDataSourceLocator &
HdInstancerTopologySchema::GetDefaultLocator()
{
    static const HdDataSourceLocator locator(
        HdInstancerTopologySchemaTokens->instancerTopology
    );
    return locator;
} 
HdInstancerTopologySchema::Builder &
HdInstancerTopologySchema::Builder::SetPrototypes(
    const HdPathArrayDataSourceHandle &prototypes)
{
    _prototypes = prototypes;
    return *this;
}

HdInstancerTopologySchema::Builder &
HdInstancerTopologySchema::Builder::SetInstanceIndices(
    const HdVectorDataSourceHandle &instanceIndices)
{
    _instanceIndices = instanceIndices;
    return *this;
}

HdInstancerTopologySchema::Builder &
HdInstancerTopologySchema::Builder::SetMask(
    const HdBoolArrayDataSourceHandle &mask)
{
    _mask = mask;
    return *this;
}

HdInstancerTopologySchema::Builder &
HdInstancerTopologySchema::Builder::SetInstanceLocations(
    const HdPathArrayDataSourceHandle &instanceLocations)
{
    _instanceLocations = instanceLocations;
    return *this;
}

HdContainerDataSourceHandle
HdInstancerTopologySchema::Builder::Build()
{
    return HdInstancerTopologySchema::BuildRetained(
        _prototypes,
        _instanceIndices,
        _mask,
        _instanceLocations
    );
}


PXR_NAMESPACE_CLOSE_SCOPE