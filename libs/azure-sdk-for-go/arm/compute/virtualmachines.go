package compute

// Copyright (c) Microsoft and contributors.  All rights reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
// http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//
// See the License for the specific language governing permissions and
// limitations under the License.
//
// Code generated by Microsoft (R) AutoRest Code Generator 0.11.0.0
// Changes may cause incorrect behavior and will be lost if the code is
// regenerated.

import (
	"github.com/nofdev/fastforward/Godeps/_workspace/src/github.com/azure/go-autorest/autorest"
	"net/http"
	"net/url"
)

// VirtualMachines Client
type VirtualMachinesClient struct {
	ComputeManagementClient
}

func NewVirtualMachinesClient(subscriptionId string) VirtualMachinesClient {
	return NewVirtualMachinesClientWithBaseUri(DefaultBaseUri, subscriptionId)
}

func NewVirtualMachinesClientWithBaseUri(baseUri string, subscriptionId string) VirtualMachinesClient {
	return VirtualMachinesClient{NewWithBaseUri(baseUri, subscriptionId)}
}

// Capture captures the VM by copying VirtualHardDisks of the VM and outputs a
// template that can be used to create similar VMs.
//
// resourceGroupName is the name of the resource group. vmName is the name of
// the virtual machine. parameters is parameters supplied to the Capture
// Virtual Machine operation.
func (client VirtualMachinesClient) Capture(resourceGroupName string, vmName string, parameters VirtualMachineCaptureParameters) (result ComputeLongRunningOperationResult, ae autorest.Error) {
	req, err := client.NewCaptureRequest(resourceGroupName, vmName, parameters)
	if err != nil {
		return result, autorest.NewErrorWithError(err, "compute.VirtualMachinesClient", "Capture", "Failure creating request")
	}

	req, err = autorest.Prepare(
		req,
		client.WithAuthorization(),
		client.WithInspection())
	if err != nil {
		return result, autorest.NewErrorWithError(err, "compute.VirtualMachinesClient", "Capture", "Failure preparing request")
	}

	resp, err := autorest.SendWithSender(client, req)
	if err == nil {
		err = client.ShouldPoll(resp)
		if err == nil {
			resp, err = client.PollAsNeeded(resp)
		}
	}

	if err == nil {
		err = autorest.Respond(
			resp,
			client.ByInspecting(),
			autorest.WithErrorUnlessOK(),
			autorest.ByUnmarshallingJSON(&result))
		if err != nil {
			ae = autorest.NewErrorWithError(err, "compute.VirtualMachinesClient", "Capture", "Failure responding to request")
		}
	} else {
		ae = autorest.NewErrorWithError(err, "compute.VirtualMachinesClient", "Capture", "Failure sending request")
	}

	autorest.Respond(resp,
		autorest.ByClosing())
	result.Response = autorest.Response{Response: resp}

	return
}

// Create the Capture request.
func (client VirtualMachinesClient) NewCaptureRequest(resourceGroupName string, vmName string, parameters VirtualMachineCaptureParameters) (*http.Request, error) {
	pathParameters := map[string]interface{}{
		"resourceGroupName": url.QueryEscape(resourceGroupName),
		"subscriptionId":    url.QueryEscape(client.SubscriptionId),
		"vmName":            url.QueryEscape(vmName),
	}

	queryParameters := map[string]interface{}{
		"api-version": ApiVersion,
	}

	return autorest.DecoratePreparer(
		client.CaptureRequestPreparer(),
		autorest.WithJSON(parameters),
		autorest.WithPathParameters(pathParameters),
		autorest.WithQueryParameters(queryParameters)).Prepare(&http.Request{})
}

// Create a Preparer by which to prepare the Capture request.
func (client VirtualMachinesClient) CaptureRequestPreparer() autorest.Preparer {
	return autorest.CreatePreparer(
		autorest.AsJSON(),
		autorest.AsPost(),
		autorest.WithBaseURL(client.BaseUri),
		autorest.WithPath("/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Compute/virtualMachines/{vmName}/capture"))
}

// CreateOrUpdate the operation to create or update a virtual machine.
//
// resourceGroupName is the name of the resource group. vmName is the name of
// the virtual machine. parameters is parameters supplied to the Create
// Virtual Machine operation.
func (client VirtualMachinesClient) CreateOrUpdate(resourceGroupName string, vmName string, parameters VirtualMachine) (result VirtualMachine, ae autorest.Error) {
	req, err := client.NewCreateOrUpdateRequest(resourceGroupName, vmName, parameters)
	if err != nil {
		return result, autorest.NewErrorWithError(err, "compute.VirtualMachinesClient", "CreateOrUpdate", "Failure creating request")
	}

	req, err = autorest.Prepare(
		req,
		client.WithAuthorization(),
		client.WithInspection())
	if err != nil {
		return result, autorest.NewErrorWithError(err, "compute.VirtualMachinesClient", "CreateOrUpdate", "Failure preparing request")
	}

	resp, err := autorest.SendWithSender(client, req)

	if err == nil {
		err = autorest.Respond(
			resp,
			client.ByInspecting(),
			autorest.WithErrorUnlessOK(),
			autorest.ByUnmarshallingJSON(&result))
		if err != nil {
			ae = autorest.NewErrorWithError(err, "compute.VirtualMachinesClient", "CreateOrUpdate", "Failure responding to request")
		}
	} else {
		ae = autorest.NewErrorWithError(err, "compute.VirtualMachinesClient", "CreateOrUpdate", "Failure sending request")
	}

	autorest.Respond(resp,
		autorest.ByClosing())
	result.Response = autorest.Response{Response: resp}

	return
}

// Create the CreateOrUpdate request.
func (client VirtualMachinesClient) NewCreateOrUpdateRequest(resourceGroupName string, vmName string, parameters VirtualMachine) (*http.Request, error) {
	pathParameters := map[string]interface{}{
		"resourceGroupName": url.QueryEscape(resourceGroupName),
		"subscriptionId":    url.QueryEscape(client.SubscriptionId),
		"vmName":            url.QueryEscape(vmName),
	}

	queryParameters := map[string]interface{}{
		"api-version": ApiVersion,
	}

	return autorest.DecoratePreparer(
		client.CreateOrUpdateRequestPreparer(),
		autorest.WithJSON(parameters),
		autorest.WithPathParameters(pathParameters),
		autorest.WithQueryParameters(queryParameters)).Prepare(&http.Request{})
}

// Create a Preparer by which to prepare the CreateOrUpdate request.
func (client VirtualMachinesClient) CreateOrUpdateRequestPreparer() autorest.Preparer {
	return autorest.CreatePreparer(
		autorest.AsJSON(),
		autorest.AsPut(),
		autorest.WithBaseURL(client.BaseUri),
		autorest.WithPath("/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Compute/virtualMachines/{vmName}"))
}

// Delete the operation to delete a virtual machine.
//
// resourceGroupName is the name of the resource group. vmName is the name of
// the virtual machine.
func (client VirtualMachinesClient) Delete(resourceGroupName string, vmName string) (result autorest.Response, ae autorest.Error) {
	req, err := client.NewDeleteRequest(resourceGroupName, vmName)
	if err != nil {
		return result, autorest.NewErrorWithError(err, "compute.VirtualMachinesClient", "Delete", "Failure creating request")
	}

	req, err = autorest.Prepare(
		req,
		client.WithAuthorization(),
		client.WithInspection())
	if err != nil {
		return result, autorest.NewErrorWithError(err, "compute.VirtualMachinesClient", "Delete", "Failure preparing request")
	}

	resp, err := autorest.SendWithSender(client, req)
	if err == nil {
		err = client.ShouldPoll(resp)
		if err == nil {
			resp, err = client.PollAsNeeded(resp)
		}
	}

	if err == nil {
		err = autorest.Respond(
			resp,
			client.ByInspecting(),
			autorest.WithErrorUnlessOK())
		if err != nil {
			ae = autorest.NewErrorWithError(err, "compute.VirtualMachinesClient", "Delete", "Failure responding to request")
		}
	} else {
		ae = autorest.NewErrorWithError(err, "compute.VirtualMachinesClient", "Delete", "Failure sending request")
	}

	autorest.Respond(resp,
		autorest.ByClosing())
	result.Response = resp

	return
}

// Create the Delete request.
func (client VirtualMachinesClient) NewDeleteRequest(resourceGroupName string, vmName string) (*http.Request, error) {
	pathParameters := map[string]interface{}{
		"resourceGroupName": url.QueryEscape(resourceGroupName),
		"subscriptionId":    url.QueryEscape(client.SubscriptionId),
		"vmName":            url.QueryEscape(vmName),
	}

	queryParameters := map[string]interface{}{
		"api-version": ApiVersion,
	}

	return autorest.DecoratePreparer(
		client.DeleteRequestPreparer(),
		autorest.WithPathParameters(pathParameters),
		autorest.WithQueryParameters(queryParameters)).Prepare(&http.Request{})
}

// Create a Preparer by which to prepare the Delete request.
func (client VirtualMachinesClient) DeleteRequestPreparer() autorest.Preparer {
	return autorest.CreatePreparer(
		autorest.AsJSON(),
		autorest.AsDelete(),
		autorest.WithBaseURL(client.BaseUri),
		autorest.WithPath("/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Compute/virtualMachines/{vmName}"))
}

// Get the operation to get a virtual machine.
//
// resourceGroupName is the name of the resource group. vmName is the name of
// the virtual machine. expand is name of the property to expand. Allowed
// value is null or 'instanceView'.
func (client VirtualMachinesClient) Get(resourceGroupName string, vmName string, expand string) (result VirtualMachine, ae autorest.Error) {
	req, err := client.NewGetRequest(resourceGroupName, vmName, expand)
	if err != nil {
		return result, autorest.NewErrorWithError(err, "compute.VirtualMachinesClient", "Get", "Failure creating request")
	}

	req, err = autorest.Prepare(
		req,
		client.WithAuthorization(),
		client.WithInspection())
	if err != nil {
		return result, autorest.NewErrorWithError(err, "compute.VirtualMachinesClient", "Get", "Failure preparing request")
	}

	resp, err := autorest.SendWithSender(client, req)

	if err == nil {
		err = autorest.Respond(
			resp,
			client.ByInspecting(),
			autorest.WithErrorUnlessOK(),
			autorest.ByUnmarshallingJSON(&result))
		if err != nil {
			ae = autorest.NewErrorWithError(err, "compute.VirtualMachinesClient", "Get", "Failure responding to request")
		}
	} else {
		ae = autorest.NewErrorWithError(err, "compute.VirtualMachinesClient", "Get", "Failure sending request")
	}

	autorest.Respond(resp,
		autorest.ByClosing())
	result.Response = autorest.Response{Response: resp}

	return
}

// Create the Get request.
func (client VirtualMachinesClient) NewGetRequest(resourceGroupName string, vmName string, expand string) (*http.Request, error) {
	pathParameters := map[string]interface{}{
		"resourceGroupName": url.QueryEscape(resourceGroupName),
		"subscriptionId":    url.QueryEscape(client.SubscriptionId),
		"vmName":            url.QueryEscape(vmName),
	}

	queryParameters := map[string]interface{}{
		"$expand":     expand,
		"api-version": ApiVersion,
	}

	return autorest.DecoratePreparer(
		client.GetRequestPreparer(),
		autorest.WithPathParameters(pathParameters),
		autorest.WithQueryParameters(queryParameters)).Prepare(&http.Request{})
}

// Create a Preparer by which to prepare the Get request.
func (client VirtualMachinesClient) GetRequestPreparer() autorest.Preparer {
	return autorest.CreatePreparer(
		autorest.AsJSON(),
		autorest.AsGet(),
		autorest.WithBaseURL(client.BaseUri),
		autorest.WithPath("/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Compute/virtualMachines/{vmName}"))
}

// Deallocate shuts down the Virtual Machine and releases the compute
// resources. You are not billed for the compute resources that this Virtual
// Machine uses.
//
// resourceGroupName is the name of the resource group. vmName is the name of
// the virtual machine.
func (client VirtualMachinesClient) Deallocate(resourceGroupName string, vmName string) (result autorest.Response, ae autorest.Error) {
	req, err := client.NewDeallocateRequest(resourceGroupName, vmName)
	if err != nil {
		return result, autorest.NewErrorWithError(err, "compute.VirtualMachinesClient", "Deallocate", "Failure creating request")
	}

	req, err = autorest.Prepare(
		req,
		client.WithAuthorization(),
		client.WithInspection())
	if err != nil {
		return result, autorest.NewErrorWithError(err, "compute.VirtualMachinesClient", "Deallocate", "Failure preparing request")
	}

	resp, err := autorest.SendWithSender(client, req)
	if err == nil {
		err = client.ShouldPoll(resp)
		if err == nil {
			resp, err = client.PollAsNeeded(resp)
		}
	}

	if err == nil {
		err = autorest.Respond(
			resp,
			client.ByInspecting(),
			autorest.WithErrorUnlessOK())
		if err != nil {
			ae = autorest.NewErrorWithError(err, "compute.VirtualMachinesClient", "Deallocate", "Failure responding to request")
		}
	} else {
		ae = autorest.NewErrorWithError(err, "compute.VirtualMachinesClient", "Deallocate", "Failure sending request")
	}

	autorest.Respond(resp,
		autorest.ByClosing())
	result.Response = resp

	return
}

// Create the Deallocate request.
func (client VirtualMachinesClient) NewDeallocateRequest(resourceGroupName string, vmName string) (*http.Request, error) {
	pathParameters := map[string]interface{}{
		"resourceGroupName": url.QueryEscape(resourceGroupName),
		"subscriptionId":    url.QueryEscape(client.SubscriptionId),
		"vmName":            url.QueryEscape(vmName),
	}

	queryParameters := map[string]interface{}{
		"api-version": ApiVersion,
	}

	return autorest.DecoratePreparer(
		client.DeallocateRequestPreparer(),
		autorest.WithPathParameters(pathParameters),
		autorest.WithQueryParameters(queryParameters)).Prepare(&http.Request{})
}

// Create a Preparer by which to prepare the Deallocate request.
func (client VirtualMachinesClient) DeallocateRequestPreparer() autorest.Preparer {
	return autorest.CreatePreparer(
		autorest.AsJSON(),
		autorest.AsPost(),
		autorest.WithBaseURL(client.BaseUri),
		autorest.WithPath("/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Compute/virtualMachines/{vmName}/deallocate"))
}

// Generalize sets the state of the VM as Generalized.
//
// resourceGroupName is the name of the resource group. vmName is the name of
// the virtual machine.
func (client VirtualMachinesClient) Generalize(resourceGroupName string, vmName string) (result autorest.Response, ae autorest.Error) {
	req, err := client.NewGeneralizeRequest(resourceGroupName, vmName)
	if err != nil {
		return result, autorest.NewErrorWithError(err, "compute.VirtualMachinesClient", "Generalize", "Failure creating request")
	}

	req, err = autorest.Prepare(
		req,
		client.WithAuthorization(),
		client.WithInspection())
	if err != nil {
		return result, autorest.NewErrorWithError(err, "compute.VirtualMachinesClient", "Generalize", "Failure preparing request")
	}

	resp, err := autorest.SendWithSender(client, req)

	if err == nil {
		err = autorest.Respond(
			resp,
			client.ByInspecting(),
			autorest.WithErrorUnlessOK())
		if err != nil {
			ae = autorest.NewErrorWithError(err, "compute.VirtualMachinesClient", "Generalize", "Failure responding to request")
		}
	} else {
		ae = autorest.NewErrorWithError(err, "compute.VirtualMachinesClient", "Generalize", "Failure sending request")
	}

	autorest.Respond(resp,
		autorest.ByClosing())
	result.Response = resp

	return
}

// Create the Generalize request.
func (client VirtualMachinesClient) NewGeneralizeRequest(resourceGroupName string, vmName string) (*http.Request, error) {
	pathParameters := map[string]interface{}{
		"resourceGroupName": url.QueryEscape(resourceGroupName),
		"subscriptionId":    url.QueryEscape(client.SubscriptionId),
		"vmName":            url.QueryEscape(vmName),
	}

	queryParameters := map[string]interface{}{
		"api-version": ApiVersion,
	}

	return autorest.DecoratePreparer(
		client.GeneralizeRequestPreparer(),
		autorest.WithPathParameters(pathParameters),
		autorest.WithQueryParameters(queryParameters)).Prepare(&http.Request{})
}

// Create a Preparer by which to prepare the Generalize request.
func (client VirtualMachinesClient) GeneralizeRequestPreparer() autorest.Preparer {
	return autorest.CreatePreparer(
		autorest.AsJSON(),
		autorest.AsPost(),
		autorest.WithBaseURL(client.BaseUri),
		autorest.WithPath("/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Compute/virtualMachines/{vmName}/generalize"))
}

// List the operation to list virtual machines under a resource group.
//
// resourceGroupName is the name of the resource group.
func (client VirtualMachinesClient) List(resourceGroupName string) (result VirtualMachineListResult, ae autorest.Error) {
	req, err := client.NewListRequest(resourceGroupName)
	if err != nil {
		return result, autorest.NewErrorWithError(err, "compute.VirtualMachinesClient", "List", "Failure creating request")
	}

	req, err = autorest.Prepare(
		req,
		client.WithAuthorization(),
		client.WithInspection())
	if err != nil {
		return result, autorest.NewErrorWithError(err, "compute.VirtualMachinesClient", "List", "Failure preparing request")
	}

	resp, err := autorest.SendWithSender(client, req)

	if err == nil {
		err = autorest.Respond(
			resp,
			client.ByInspecting(),
			autorest.WithErrorUnlessOK(),
			autorest.ByUnmarshallingJSON(&result))
		if err != nil {
			ae = autorest.NewErrorWithError(err, "compute.VirtualMachinesClient", "List", "Failure responding to request")
		}
	} else {
		ae = autorest.NewErrorWithError(err, "compute.VirtualMachinesClient", "List", "Failure sending request")
	}

	autorest.Respond(resp,
		autorest.ByClosing())
	result.Response = autorest.Response{Response: resp}

	return
}

// Create the List request.
func (client VirtualMachinesClient) NewListRequest(resourceGroupName string) (*http.Request, error) {
	pathParameters := map[string]interface{}{
		"resourceGroupName": url.QueryEscape(resourceGroupName),
		"subscriptionId":    url.QueryEscape(client.SubscriptionId),
	}

	queryParameters := map[string]interface{}{
		"api-version": ApiVersion,
	}

	return autorest.DecoratePreparer(
		client.ListRequestPreparer(),
		autorest.WithPathParameters(pathParameters),
		autorest.WithQueryParameters(queryParameters)).Prepare(&http.Request{})
}

// Create a Preparer by which to prepare the List request.
func (client VirtualMachinesClient) ListRequestPreparer() autorest.Preparer {
	return autorest.CreatePreparer(
		autorest.AsJSON(),
		autorest.AsGet(),
		autorest.WithBaseURL(client.BaseUri),
		autorest.WithPath("/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Compute/virtualMachines"))
}

// ListAll gets the list of Virtual Machines in the subscription. Use nextLink
// property in the response to get the next page of Virtual Machines. Do this
// till nextLink is not null to fetch all the Virtual Machines.
func (client VirtualMachinesClient) ListAll() (result VirtualMachineListResult, ae autorest.Error) {
	req, err := client.NewListAllRequest()
	if err != nil {
		return result, autorest.NewErrorWithError(err, "compute.VirtualMachinesClient", "ListAll", "Failure creating request")
	}

	req, err = autorest.Prepare(
		req,
		client.WithAuthorization(),
		client.WithInspection())
	if err != nil {
		return result, autorest.NewErrorWithError(err, "compute.VirtualMachinesClient", "ListAll", "Failure preparing request")
	}

	resp, err := autorest.SendWithSender(client, req)

	if err == nil {
		err = autorest.Respond(
			resp,
			client.ByInspecting(),
			autorest.WithErrorUnlessOK(),
			autorest.ByUnmarshallingJSON(&result))
		if err != nil {
			ae = autorest.NewErrorWithError(err, "compute.VirtualMachinesClient", "ListAll", "Failure responding to request")
		}
	} else {
		ae = autorest.NewErrorWithError(err, "compute.VirtualMachinesClient", "ListAll", "Failure sending request")
	}

	autorest.Respond(resp,
		autorest.ByClosing())
	result.Response = autorest.Response{Response: resp}

	return
}

// Create the ListAll request.
func (client VirtualMachinesClient) NewListAllRequest() (*http.Request, error) {
	pathParameters := map[string]interface{}{
		"subscriptionId": url.QueryEscape(client.SubscriptionId),
	}

	queryParameters := map[string]interface{}{
		"api-version": ApiVersion,
	}

	return autorest.DecoratePreparer(
		client.ListAllRequestPreparer(),
		autorest.WithPathParameters(pathParameters),
		autorest.WithQueryParameters(queryParameters)).Prepare(&http.Request{})
}

// Create a Preparer by which to prepare the ListAll request.
func (client VirtualMachinesClient) ListAllRequestPreparer() autorest.Preparer {
	return autorest.CreatePreparer(
		autorest.AsJSON(),
		autorest.AsGet(),
		autorest.WithBaseURL(client.BaseUri),
		autorest.WithPath("/subscriptions/{subscriptionId}/providers/Microsoft.Compute/virtualMachines"))
}

// ListAvailableSizes lists virtual-machine-sizes available to be used for a
// virtual machine.
//
// resourceGroupName is the name of the resource group. vmName is the name of
// the virtual machine.
func (client VirtualMachinesClient) ListAvailableSizes(resourceGroupName string, vmName string) (result VirtualMachineSizeListResult, ae autorest.Error) {
	req, err := client.NewListAvailableSizesRequest(resourceGroupName, vmName)
	if err != nil {
		return result, autorest.NewErrorWithError(err, "compute.VirtualMachinesClient", "ListAvailableSizes", "Failure creating request")
	}

	req, err = autorest.Prepare(
		req,
		client.WithAuthorization(),
		client.WithInspection())
	if err != nil {
		return result, autorest.NewErrorWithError(err, "compute.VirtualMachinesClient", "ListAvailableSizes", "Failure preparing request")
	}

	resp, err := autorest.SendWithSender(client, req)

	if err == nil {
		err = autorest.Respond(
			resp,
			client.ByInspecting(),
			autorest.WithErrorUnlessOK(),
			autorest.ByUnmarshallingJSON(&result))
		if err != nil {
			ae = autorest.NewErrorWithError(err, "compute.VirtualMachinesClient", "ListAvailableSizes", "Failure responding to request")
		}
	} else {
		ae = autorest.NewErrorWithError(err, "compute.VirtualMachinesClient", "ListAvailableSizes", "Failure sending request")
	}

	autorest.Respond(resp,
		autorest.ByClosing())
	result.Response = autorest.Response{Response: resp}

	return
}

// Create the ListAvailableSizes request.
func (client VirtualMachinesClient) NewListAvailableSizesRequest(resourceGroupName string, vmName string) (*http.Request, error) {
	pathParameters := map[string]interface{}{
		"resourceGroupName": url.QueryEscape(resourceGroupName),
		"subscriptionId":    url.QueryEscape(client.SubscriptionId),
		"vmName":            url.QueryEscape(vmName),
	}

	queryParameters := map[string]interface{}{
		"api-version": ApiVersion,
	}

	return autorest.DecoratePreparer(
		client.ListAvailableSizesRequestPreparer(),
		autorest.WithPathParameters(pathParameters),
		autorest.WithQueryParameters(queryParameters)).Prepare(&http.Request{})
}

// Create a Preparer by which to prepare the ListAvailableSizes request.
func (client VirtualMachinesClient) ListAvailableSizesRequestPreparer() autorest.Preparer {
	return autorest.CreatePreparer(
		autorest.AsJSON(),
		autorest.AsGet(),
		autorest.WithBaseURL(client.BaseUri),
		autorest.WithPath("/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Compute/virtualMachines/{vmName}/vmSizes"))
}

// PowerOff the operation to power off (stop) a virtual machine.
//
// resourceGroupName is the name of the resource group. vmName is the name of
// the virtual machine.
func (client VirtualMachinesClient) PowerOff(resourceGroupName string, vmName string) (result autorest.Response, ae autorest.Error) {
	req, err := client.NewPowerOffRequest(resourceGroupName, vmName)
	if err != nil {
		return result, autorest.NewErrorWithError(err, "compute.VirtualMachinesClient", "PowerOff", "Failure creating request")
	}

	req, err = autorest.Prepare(
		req,
		client.WithAuthorization(),
		client.WithInspection())
	if err != nil {
		return result, autorest.NewErrorWithError(err, "compute.VirtualMachinesClient", "PowerOff", "Failure preparing request")
	}

	resp, err := autorest.SendWithSender(client, req)
	if err == nil {
		err = client.ShouldPoll(resp)
		if err == nil {
			resp, err = client.PollAsNeeded(resp)
		}
	}

	if err == nil {
		err = autorest.Respond(
			resp,
			client.ByInspecting(),
			autorest.WithErrorUnlessOK())
		if err != nil {
			ae = autorest.NewErrorWithError(err, "compute.VirtualMachinesClient", "PowerOff", "Failure responding to request")
		}
	} else {
		ae = autorest.NewErrorWithError(err, "compute.VirtualMachinesClient", "PowerOff", "Failure sending request")
	}

	autorest.Respond(resp,
		autorest.ByClosing())
	result.Response = resp

	return
}

// Create the PowerOff request.
func (client VirtualMachinesClient) NewPowerOffRequest(resourceGroupName string, vmName string) (*http.Request, error) {
	pathParameters := map[string]interface{}{
		"resourceGroupName": url.QueryEscape(resourceGroupName),
		"subscriptionId":    url.QueryEscape(client.SubscriptionId),
		"vmName":            url.QueryEscape(vmName),
	}

	queryParameters := map[string]interface{}{
		"api-version": ApiVersion,
	}

	return autorest.DecoratePreparer(
		client.PowerOffRequestPreparer(),
		autorest.WithPathParameters(pathParameters),
		autorest.WithQueryParameters(queryParameters)).Prepare(&http.Request{})
}

// Create a Preparer by which to prepare the PowerOff request.
func (client VirtualMachinesClient) PowerOffRequestPreparer() autorest.Preparer {
	return autorest.CreatePreparer(
		autorest.AsJSON(),
		autorest.AsPost(),
		autorest.WithBaseURL(client.BaseUri),
		autorest.WithPath("/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Compute/virtualMachines/{vmName}/powerOff"))
}

// Restart the operation to restart a virtual machine.
//
// resourceGroupName is the name of the resource group. vmName is the name of
// the virtual machine.
func (client VirtualMachinesClient) Restart(resourceGroupName string, vmName string) (result autorest.Response, ae autorest.Error) {
	req, err := client.NewRestartRequest(resourceGroupName, vmName)
	if err != nil {
		return result, autorest.NewErrorWithError(err, "compute.VirtualMachinesClient", "Restart", "Failure creating request")
	}

	req, err = autorest.Prepare(
		req,
		client.WithAuthorization(),
		client.WithInspection())
	if err != nil {
		return result, autorest.NewErrorWithError(err, "compute.VirtualMachinesClient", "Restart", "Failure preparing request")
	}

	resp, err := autorest.SendWithSender(client, req)
	if err == nil {
		err = client.ShouldPoll(resp)
		if err == nil {
			resp, err = client.PollAsNeeded(resp)
		}
	}

	if err == nil {
		err = autorest.Respond(
			resp,
			client.ByInspecting(),
			autorest.WithErrorUnlessOK())
		if err != nil {
			ae = autorest.NewErrorWithError(err, "compute.VirtualMachinesClient", "Restart", "Failure responding to request")
		}
	} else {
		ae = autorest.NewErrorWithError(err, "compute.VirtualMachinesClient", "Restart", "Failure sending request")
	}

	autorest.Respond(resp,
		autorest.ByClosing())
	result.Response = resp

	return
}

// Create the Restart request.
func (client VirtualMachinesClient) NewRestartRequest(resourceGroupName string, vmName string) (*http.Request, error) {
	pathParameters := map[string]interface{}{
		"resourceGroupName": url.QueryEscape(resourceGroupName),
		"subscriptionId":    url.QueryEscape(client.SubscriptionId),
		"vmName":            url.QueryEscape(vmName),
	}

	queryParameters := map[string]interface{}{
		"api-version": ApiVersion,
	}

	return autorest.DecoratePreparer(
		client.RestartRequestPreparer(),
		autorest.WithPathParameters(pathParameters),
		autorest.WithQueryParameters(queryParameters)).Prepare(&http.Request{})
}

// Create a Preparer by which to prepare the Restart request.
func (client VirtualMachinesClient) RestartRequestPreparer() autorest.Preparer {
	return autorest.CreatePreparer(
		autorest.AsJSON(),
		autorest.AsPost(),
		autorest.WithBaseURL(client.BaseUri),
		autorest.WithPath("/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Compute/virtualMachines/{vmName}/restart"))
}

// Start the operation to start a virtual machine.
//
// resourceGroupName is the name of the resource group. vmName is the name of
// the virtual machine.
func (client VirtualMachinesClient) Start(resourceGroupName string, vmName string) (result autorest.Response, ae autorest.Error) {
	req, err := client.NewStartRequest(resourceGroupName, vmName)
	if err != nil {
		return result, autorest.NewErrorWithError(err, "compute.VirtualMachinesClient", "Start", "Failure creating request")
	}

	req, err = autorest.Prepare(
		req,
		client.WithAuthorization(),
		client.WithInspection())
	if err != nil {
		return result, autorest.NewErrorWithError(err, "compute.VirtualMachinesClient", "Start", "Failure preparing request")
	}

	resp, err := autorest.SendWithSender(client, req)
	if err == nil {
		err = client.ShouldPoll(resp)
		if err == nil {
			resp, err = client.PollAsNeeded(resp)
		}
	}

	if err == nil {
		err = autorest.Respond(
			resp,
			client.ByInspecting(),
			autorest.WithErrorUnlessOK())
		if err != nil {
			ae = autorest.NewErrorWithError(err, "compute.VirtualMachinesClient", "Start", "Failure responding to request")
		}
	} else {
		ae = autorest.NewErrorWithError(err, "compute.VirtualMachinesClient", "Start", "Failure sending request")
	}

	autorest.Respond(resp,
		autorest.ByClosing())
	result.Response = resp

	return
}

// Create the Start request.
func (client VirtualMachinesClient) NewStartRequest(resourceGroupName string, vmName string) (*http.Request, error) {
	pathParameters := map[string]interface{}{
		"resourceGroupName": url.QueryEscape(resourceGroupName),
		"subscriptionId":    url.QueryEscape(client.SubscriptionId),
		"vmName":            url.QueryEscape(vmName),
	}

	queryParameters := map[string]interface{}{
		"api-version": ApiVersion,
	}

	return autorest.DecoratePreparer(
		client.StartRequestPreparer(),
		autorest.WithPathParameters(pathParameters),
		autorest.WithQueryParameters(queryParameters)).Prepare(&http.Request{})
}

// Create a Preparer by which to prepare the Start request.
func (client VirtualMachinesClient) StartRequestPreparer() autorest.Preparer {
	return autorest.CreatePreparer(
		autorest.AsJSON(),
		autorest.AsPost(),
		autorest.WithBaseURL(client.BaseUri),
		autorest.WithPath("/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Compute/virtualMachines/{vmName}/start"))
}
