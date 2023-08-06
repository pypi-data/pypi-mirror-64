# mygp Command Line Interface - how to use

## 1. Setting authentication parameters

Before you can execute any requests on mygp, you need to configure the basic
 authentication parameters so an access token can be obtained from the server. 
 You can do this either by using `mygp-cli set-auth` command or manually 
 (see below)
 
### `set-auth` command
 
Using the `set-auth` command, you can specify one or more authentication
 parameters that will be used to request an authentication token. Here is an
 example of how to set all of the required authentication parameters at once:

```bash
mygp-cli set-auth \
 --api-url https://uat1-api.mygp.cz \
 --auth-url https://uat1.mygp.cz/auth \
 --realm mygp-cz \
 --cid some-client \
 --secret be1ee039-cbe0-4f47-8d4f-2c5e68a21744
```

The command then saves these parameters in the `~/.mygp/state.json` state file
(`~` denoting the user's home directory). Note that all of the parameters of 
 the command are optional, so you can use the the `set-auth` command later to 
 just update one or more of them.

## 2. Requesting an access token

Once the authentication parameters have been set, you can request an access
 token from the server using the `get-token` command:
 
```bash
mygp-cli get-token
```

If the request was successful, a newly generated access token will be saved
 to the `~/.mygp/state.json` state file to be used by subsequent commands.
 

## 3. Creating a sandbox customer

The next step is to create a sandbox customer:
 
```bash
mygp-cli add-customer
```

Once the customer has been created, its `customer_key` will be stored in the 
state file so it can be used by subsequent commands without having to copy-paste
it as a command line argument.

### Specifying gateways and outlets

Optionally, you can specify IDs of customer gateways and/or outlets when 
creating a new customer:

```bash
mygp-cli add-customer \
  --gateways PGWMID99003 PGWMID99004 PGWMID99005 \
  --outlets OUTMID99001 OUTMID99002
```

If you do not specify gateways and outlets, they will be created automatically
for you. You can also add gateways and outlets to an existing customer later (
please see the following sections).

## 4. Adding gateways to an existing customer

You can add outlets to an existing customer using the `add-gateways` command.
Example:

```bash
mygp-cli add-gateways \
  --customer 689ab75a767e7349d409a5a720fc2e525898f7a2 \
  --gateways PGWMID99003 PGWMID99004 PGWMID99005
```

`--customer` parameter is optional: if you do not specify it, the command will
use the last `customer_key` value from the state file.

## 5. Adding outlets to an existing customer

You can add outlets to an existing customer using the `add-outlets` command.
Example:

```bash
mygp-cli add-outlets \
  --customer 689ab75a767e7349d409a5a720fc2e525898f7a2 \
  --outlets OUTMID99001 OUTMID99002
```

`--customer` parameter is optional: if you do not specify it, the command will
use the last `customer_key` value from the state file.
