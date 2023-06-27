import bitcoin.wallet

WIF_private_key = "92uLz2m5S89jQoFbX88fjudD4dZwjMdpBnut4ZbvX73c58nGPBm"

bitcoin.SelectParams("testnet")  # Select the network (testnet or mainnet)
my_private_key = bitcoin.wallet.CBitcoinSecret(WIF_private_key)
my_public_key = my_private_key.pub

first_person_private_key = bitcoin.wallet.CBitcoinSecret("92W78XPjA2fTR4qGcFQed5bAv19mJZkzDkXRLHyZob3DBRMgiPU")
first_person_public_key = first_person_private_key.pub

second_person_private_key = bitcoin.wallet.CBitcoinSecret("92Y775cuvvvdjsoiRdu3ntEV3d22Zk1AR1HvqR2DDU8HCW1xkRo")
second_person_public_key = second_person_private_key.pub

third_person_private_key = bitcoin.wallet.CBitcoinSecret("93TgTKfXUyTEcGXsWjuwptBs9XgoXrfb1vw6AJpi68a3eQbz3aa")
third_person_public_key = third_person_private_key.pub
