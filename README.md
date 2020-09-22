# Using service accounts with Python

This example shows two ways of authenticating to OpenShift using service
accounts.

## About the code

### Version 1

The `v1` method uses the `openshift` module to automatically configure
authentication and interact with the OpenShift API.

### Version 2

The `v2` method uses the `requests` module. It retrieves the token, the CA
certificate, and the Kubernetes API url from data in the environment:

- The token and ca certificate are provided by the secret and are located
  in `/run/secrets/kubernetes.io/serviceaccount`,

- We use the magic name `kubernetes.default.svc` to access the Kubernetes API,
  which will map to a cluster local ip address at which we can access the API
  via https.

## Deploying

1. Edit `k8s/kustomization.yml` and set `namespace` to the name of the
   namespace into which you want to deploy.

1. Run `oc apply -k k8s`

The above steps will create:

- a service account
- a `RoleBinding` granting the service account admin privileges on the
  project
- A `Deployment` resource
- A `Service`
- A `Route`

## See also

- https://kubernetes.io/docs/tasks/administer-cluster/access-cluster-api/
