module.exports = {
  // See <http://truffleframework.com/docs/advanced/configuration>
  // for more about customizing your Truffle configuration!
  networks: {
    development: {
      host: "10.0.0.20",
      port: 8545,
      network_id: "*" // Match any network id
    }
  },
	compilers: {
     solc: {
       version: "0.4.20"  // ex:  "0.4.20". (Default: Truffle's installed solc)
     }
  }
};

