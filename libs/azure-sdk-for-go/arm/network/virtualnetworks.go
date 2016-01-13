package network

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

// VirtualNetworks Client
type VirtualNetworksClient struct {
	NetworkResourceProviderClient
}

func NewVirtualNetworksClient(subscriptionId string) VirtualNetworksClient {
	return NewVirtualNetworksClientWithBaseUri(DefaultBaseUri, subscriptionId)
}

func NewVirtualNetworksClientWithBaseUri(baseUri string, subscriptionId string) VirtualNetworksClient {
	return VirtualNetworksClient{NewWithBaseUri(baseUri, subscriptionId)}
}

// Delete the Delete VirtualNetwork operation deletes the specifed virtual
// network
//
// resourceGroupName is the name of the resource group. virtualNetworkName is
// the name of the virtual network.
func (client VirtualNetworksClient) Delete(resourceGroupName string, virtualNetworkName string) (result autorest.Response, ae autorest.Error) {
	req, err := client.NewDeleteRequest(resourceGroupName, virtualNetworkName)
	if err != nil {
		return result, autorest.NewErrorWithError(err, "network.VirtualNetworksClient", "Delete", "Failure creating request")
	}

	req, err = autorest.Prepare(
		req,
		client.WithAuthorization(),
		client.WithInspection())
	if err != nil {
		return result, autorest.NewErrorWithError(err, "network.VirtualNetworksClient", "Delete", "Failure preparing request")
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
			ae = autorest.NewErrorWithError(err, "network.VirtualNetworksClient", "Delete", "Failure responding to request")
		}
	} else {
		ae = autorest.NewErrorWithError(err, "network.VirtualNetworksClient", "Delete", "Failure sending request")
	}

	autorest.Respond(resp,
		autorest.ByClosing())
	result.Response = resp

	return
}

// Create the Delete request.
func (client VirtualNetworksClient) NewDeleteRequest(resourceGroupName string, virtualNetworkName string) (*http.Request, error) {
	pathParameters := map[string]interface{}{
		"resourceGroupName":  url.QueryEscape(resourceGroupName),
		"subscriptionId":     url.QueryEscape(client.SubscriptionId),
		"virtualNetworkName": url.QueryEscape(virtualNetworkName),
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
func (client VirtualNetworksClient) DeleteRequestPreparer() autorest.Preparer {
	return autorest.CreatePreparer(
		autorest.AsJSON(),
		autorest.AsDelete(),
		autorest.WithBaseURL(client.BaseUri),
		autorest.WithPath("/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/virtualnetworks/{virtualNetworkName}"))
}

// Get the Get VirtualNetwork operation retrieves information about the
// specified virtual network.
//
// resourceGroupName is the name of the resource group. virtualNetworkName is
// the name of the virtual network.
func (client VirtualNetworksClient) Get(resourceGroupName string, virtualNetworkName string) (result VirtualNetwork, ae autorest.Error) {
	req, err := client.NewGetRequest(resourceGroupName, virtualNetworkName)
	if err != nil {
		return result, autorest.NewErrorWithError(err, "network.VirtualNetworksClient", "Get", "Failure creating request")
	}

	req, err = autorest.Prepare(
		req,
		client.WithAuthorization(),
		client.WithInspection())
	if err != nil {
		return result, autorest.NewErrorWithError(err, "network.VirtualNetworksClient", "Get", "Failure preparing request")
	}

	resp, err := autorest.SendWithSender(client, req)

	if err == nil {
		err = autorest.Respond(
			resp,
			client.ByInspecting(),
			autorest.WithErrorUnlessOK(),
			autorest.ByUnmarshallingJSON(&result))
		if err != nil {
			ae = autorest.NewErrorWithError(err, "network.VirtualNetworksClient", "Get", "Failure responding to request")
		}
	} else {
		ae = autorest.NewErrorWithError(err, "network.VirtualNetworksClient", "Get", "Failure sending request")
	}

	autorest.Respond(resp,
		autorest.ByClosing())
	result.Response = autorest.Response{Response: resp}

	return
}

// Create the Get request.
func (client VirtualNetworksClient) NewGetRequest(resourceGroupName string, virtualNetworkName string) (*http.Request, error) {
	pathParameters := map[string]interface{}{
		"resourceGroupName":  url.QueryEscape(resourceGroupName),
		"subscriptionId":     url.QueryEscape(client.SubscriptionId),
		"virtualNetworkName": url.QueryEscape(virtualNetworkName),
	}

	queryParameters := map[string]interface{}{
		"api-version": ApiVersion,
	}

	return autorest.DecoratePreparer(
		client.GetRequestPreparer(),
		autorest.WithPathParameters(pathParameters),
		autorest.WithQueryParameters(queryParameters)).Prepare(&http.Request{})
}

// Create a Preparer by which to prepare the Get request.
func (client VirtualNetworksClient) GetRequestPreparer() autorest.Preparer {
	return autorest.CreatePreparer(
		autorest.AsJSON(),
		autorest.AsGet(),
		autorest.WithBaseURL(client.BaseUri),
		autorest.WithPath("/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/virtualnetworks/{virtualNetworkName}"))
}

// CreateOrUpdate the Put VirtualNetwork operation creates/updates a virtual
// network in the specified resource group.
//
// resourceGroupName is the name of the resource group. virtualNetworkName is
// the name of the virtual network. parameters is parameters supplied to the
// create/update Virtual Network operation
func (client VirtualNetworksClient) CreateOrUpdate(resourceGroupName string, virtualNetworkName string, parameters VirtualNetwork) (result VirtualNetwork, ae autorest.Error) {
	req, err := client.NewCreateOrUpdateRequest(resourceGroupName, virtualNetworkName, parameters)
	if err != nil {
		return result, autorest.NewErrorWithError(err, "network.VirtualNetworksClient", "CreateOrUpdate", "Failure creating request")
	}

	req, err = autorest.Prepare(
		req,
		client.WithAuthorization(),
		client.WithInspection())
	if err != nil {
		return result, autorest.NewErrorWithError(err, "network.VirtualNetworksClient", "CreateOrUpdate", "Failure preparing request")
	}

	resp, err := autorest.SendWithSender(client, req)

	if err == nil {
		err = autorest.Respond(
			resp,
			client.ByInspecting(),
			autorest.WithErrorUnlessOK(),
			autorest.ByUnmarshallingJSON(&result))
		if err != nil {
			ae = autorest.NewErrorWithError(err, "network.VirtualNetworksClient", "CreateOrUpdate", "Failure responding to request")
		}
	} else {
		ae = autorest.NewErrorWithError(err, "network.VirtualNetworksClient", "CreateOrUpdate", "Failure sending request")
	}

	autorest.Respond(resp,
		autorest.ByClosing())
	result.Response = autorest.Response{Response: resp}

	return
}

// Create the CreateOrUpdate request.
func (client VirtualNetworksClient) NewCreateOrUpdateRequest(resourceGroupName string, virtualNetworkName string, parameters VirtualNetwork) (*http.Request, error) {
	pathParameters := map[string]interface{}{
		"resourceGroupName":  url.QueryEscape(resourceGroupName),
		"subscriptionId":     url.QueryEscape(client.SubscriptionId),
		"virtualNetworkName": url.QueryEscape(virtualNetworkName),
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
func (client VirtualNetworksClient) CreateOrUpdateRequestPreparer() autorest.Preparer {
	return autorest.CreatePreparer(
		autorest.AsJSON(),
		autorest.AsPut(),
		autorest.WithBaseURL(client.BaseUri),
		autorest.WithPath("/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/virtualnetworks/{virtualNetworkName}"))
}

// ListAll the list VirtualNetwork returns all Virtual Networks in a
// subscription
func (client VirtualNetworksClient) ListAll() (result VirtualNetworkListResult, ae autorest.Error) {
	req, err := client.NewListAllRequest()
	if err != nil {
		return result, autorest.NewErrorWithError(err, "network.VirtualNetworksClient", "ListAll", "Failure creating request")
	}

	req, err = autorest.Prepare(
		req,
		client.WithAuthorization(),
		client.WithInspection())
	if err != nil {
		return result, autorest.NewErrorWithError(err, "network.VirtualNetworksClient", "ListAll", "Failure preparing request")
	}

	resp, err := autorest.SendWithSender(client, req)

	if err == nil {
		err = autorest.Respond(
			resp,
			client.ByInspecting(),
			autorest.WithErrorUnlessOK(),
			autorest.ByUnmarshallingJSON(&result))
		if err != nil {
			ae = autorest.NewErrorWithError(err, "network.VirtualNetworksClient", "ListAll", "Failure responding to request")
		}
	} else {
		ae = autorest.NewErrorWithError(err, "network.VirtualNetworksClient", "ListAll", "Failure sending request")
	}

	autorest.Respond(resp,
		autorest.ByClosing())
	result.Response = autorest.Response{Response: resp}

	return
}

// Create the ListAll request.
func (client VirtualNetworksClient) NewListAllRequest() (*http.Request, error) {
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
func (client VirtualNetworksClient) ListAllRequestPreparer() autorest.Preparer {
	return autorest.CreatePreparer(
		autorest.AsJSON(),
		autorest.AsGet(),
		autorest.WithBaseURL(client.BaseUri),
		autorest.WithPath("/subscriptions/{subscriptionId}/providers/Microsoft.Network/virtualnetworks"))
}

// List the list VirtualNetwork returns all Virtual Networks in a resource
// group
//
// resourceGroupName is the name of the resource group.
func (client VirtualNetworksClient) List(resourceGroupName string) (result VirtualNetworkListResult, ae autorest.Error) {
	req, err := client.NewListRequest(resourceGroupName)
	if err != nil {
		return result, autorest.NewErrorWithError(err, "network.VirtualNetworksClient", "List", "Failure creating request")
	}

	req, err = autorest.Prepare(
		req,
		client.WithAuthorization(),
		client.WithInspection())
	if err != nil {
		return result, autorest.NewErrorWithError(err, "network.VirtualNetworksClient", "List", "Failure preparing request")
	}

	resp, err := autorest.SendWithSender(client, req)

	if err == nil {
		err = autorest.Respond(
			resp,
			client.ByInspecting(),
			autorest.WithErrorUnlessOK(),
			autorest.ByUnmarshallingJSON(&result))
		if err != nil {
			ae = autorest.NewErrorWithError(err, "network.VirtualNetworksClient", "List", "Failure responding to request")
		}
	} else {
		ae = autorest.NewErrorWithError(err, "network.VirtualNetworksClient", "List", "Failure sending request")
	}

	autorest.Respond(resp,
		autorest.ByClosing())
	result.Response = autorest.Response{Response: resp}

	return
}

// Create the List request.
func (client VirtualNetworksClient) NewListRequest(resourceGroupName string) (*http.Request, error) {
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
func (client VirtualNetworksClient) ListRequestPreparer() autorest.Preparer {
	return autorest.CreatePreparer(
		autorest.AsJSON(),
		autorest.AsGet(),
		autorest.WithBaseURL(client.BaseUri),
		autorest.WithPath("/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/virtualnetworks"))
}
