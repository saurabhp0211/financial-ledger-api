The Gateway Check (schemas.py): The user sends raw JSON data over the internet. FastAPI instantly forces this data through schemas.ExpenseCreate. If the user sent a negative number for amount, Pydantic catches it immediately and rejects the request at the gate with a 422 Unprocessable Entity response. Your database never even knows it happened.

The Routing Decision (main.py): If the data structure matches your schema perfectly, it drops into your endpoint function inside main.py.

The Identity Guard (utils.py / main.py): Your endpoint sees Depends(get_current_user). It grabs the incoming cryptographic token from the request headers, decrypts it using your secret key, extracts the user's identity email, and fetches their corresponding record from the database.

The Pipeline Allocation (database.py): Your endpoint calls Depends(get_db). This opens a temporary, safe connection pipeline directly to your expenses.db file so data can be written securely.

The Storage Generation (models.py): Your code initializes a row object: models.Expense(...). SQLAlchemy reads your model configurations to translate your Python properties into raw SQL insert commands.

The Commit: db.commit() pushes the row down the pipeline, and the data is permanently etched onto the disk within your SQLite database.



This is an extremely difficult assignment.

You may have never heard of blockchain, Rust, Substreams, or Solana before. Most candidates haven't. That's intentional.

We WANT you to use AI tools. Use ChatGPT, Claude, Copilot, Gemini, or any AI assistant you prefer. Use Google, Stack Overflow, GitHub, official docs—whatever helps you succeed.

Why are we doing this?

We're evaluating how you perform when faced with a hard, ambiguous task in unfamiliar territory. We want to see:

How you break down a complex problem
How effectively you leverage AI and other resources
How you persist through challenges
Your problem-solving approach
Making good progress on this assignment often means we instantly hire you. This is not an exaggeration—candidates who demonstrate strong problem-solving with unfamiliar technologies stand out significantly.

All we need from you: Don't give up. Try your best.

Your first goal is to make sense of the assignment, then execute it with AI assistance.

Overview
Your goal is to create a Substreams SPKG file that extracts transfer actions from the Solana blockchain.

You must extract transfers for Solana blocks 385870151 to 385870156.

Required Output Format
Each transfer message must be in this exact JSON format:

{"from": "Eq1c3uNugn3FRpJ99K2q1ZyQrora3jntUqvkMnGroKkB", "to": "4XpSNfoNfireSgdg8hY6Ng3dWrHjewZhmCancypjbcCN", "amount": 325253}
Where:

from - The sender's Solana wallet address (base58 encoded)
to - The recipient's Solana wallet address (base58 encoded)
amount - The transfer amount (as an integer)
Important: A single block can contain multiple transfers. Your output should include one JSON object per transfer found in each block. For example, if block 385870151 has 5 transfers, you should output 5 separate JSON messages for that block.

What You Need To Do
Step 1: Install Rust
You must use Rust to build the Substreams SPKG package—this is mandatory.

We understand you may have never heard of Rust before. That's exactly the point. We want to see how you thrive in an unknown language using AI tools. Many successful candidates have completed this assignment without any prior Rust experience.

Figure out how to install Rust on your system.

Step 2: Install the Substreams CLI
Go to the Substreams documentation and figure out how to install the CLI.

We evaluate whether you can navigate documentation and figure out installation on your own.

Step 3: Get a Free API Key
You need an API key to stream data from a Substreams provider. Figure out how to obtain one.

Step 4: Develop Your Substreams Module
You need to create a Rust-based Substreams module that:

Processes Solana blocks
Extracts transfer instructions
Outputs each transfer in the required format
This will involve:

Setting up a Rust project
Creating a substreams.yaml manifest
Writing protobuf definitions
Implementing your map module in Rust
Step 5: Build the SPKG File
Package your module into an SPKG file.

Step 6: Run and Verify
Run your Substreams against blocks 385870151 to 385870156 and verify the output matches the required format.

Success Criteria
To successfully complete this assignment, you must:

Build a valid SPKG file - The package must compile without errors
Run the Substreams - Successfully execute against blocks 385870151-385870156
Output correct format - Each transfer must be formatted as:
{"from": "Eq1c3uNugn3FRpJ99K2q1ZyQrora3jntUqvkMnGroKkB", "to": "4XpSNfoNfireSgdg8hY6Ng3dWrHjewZhmCancypjbcCN", "amount": 325253}
Tips for Success
Start with understanding - Spend time reading documentation before coding
Use AI effectively - Ask AI tools to explain concepts, debug errors, and suggest code
Work incrementally - Get a basic version working first, then refine
Read error messages - They often tell you exactly what's wrong
Final Notes
Remember: We're not expecting perfection. We want to see your problem-solving process, how you handle ambiguity, and how effectively you use available tools and resources.

Don't give up. Try your best. Good luck!



Soln 
Here's the plan, then everything you need to type. Installs take the longest, so start Step 1 right away and read the rest while they run.

What the task actually is
Substreams lets you write a Rust function (a "map module"). It's compiled to WASM, the provider runs it on every blockchain block, and it streams your output back to you.
SPKG is the packaged bundle of the manifest, the WASM and the protobuf definitions.
A SOL transfer on Solana is a System Program instruction (program id 111…1). The first 4 bytes of the instruction data say which instruction it is (2 means Transfer), and the next 8 bytes are the amount in lamports. Account 0 is the sender and account 1 is the recipient.
Scope decision: native SOL transfers, since the brief says "wallet address". These details make it "close to perfect":

Read both top-level and inner instructions. Programs move SOL through inner calls (CPI).
Skip failed transactions, because their transfers never happened.
Resolve accounts from address lookup tables (v0 transactions) as well.
Handle TransferWithSeed as well as Transfer.
Time budget
Min	Step
0–10	Installs and API key (in parallel)
10–15	Scaffold the project, first build
15–35	Type the code, build, fix errors
35–45	Run blocks 385870151–156, format, verify
45–60	README, push, submit
Keep a one-line note of every error you hit and how you fixed it. It goes into the README, and showing how you push through problems is part of what they're grading.

Step 1: installs (open 2 terminal tabs)
Tab 1, Rust:


curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
Press Enter for the default install. Then:


source "$HOME/.cargo/env"
rustup target add wasm32-unknown-unknown
cargo --version
Tab 2, Substreams CLI and buf (buf is used to generate the Rust code from the .proto file):


brew install streamingfast/tap/substreams
brew install bufbuild/buf/buf
substreams --version
jq --version
If jq is missing: brew install jq.
If brew is missing, tell me.
Step 2: API key (browser, while the installs run)
Go to docs.substreams.dev and find the authentication page. It sends you to The Graph Market (thegraph.market). Sign up there and create an API key. Don't paste the key anywhere else, including to me.

Step 3: scaffold and baseline (Tab 2)

cd ~
substreams init
Choose Solana, then the minimal template (named something like sol-minimal). Name the project solana_transfers. Then:


cd solana_transfers
substreams auth
. ./.substreams.env
echo ".substreams.env" >> .gitignore
echo "target/" >> .gitignore
substreams build
substreams auth walks you through pasting the token and saves it to .substreams.env. The first build takes 2–4 minutes; type Step 4 while it compiles.

Then run a test on one block. Use the template's module name, which you'll find under modules: → name: in substreams.yaml:


substreams run -e mainnet.sol.streamingfast.io:443 substreams.yaml <template_module_name> -s 385870151 -t +1
If this prints data, your auth, endpoint and build all work. If init or build fails, tell me the error. I have the fully manual files ready as a fallback.

Step 4: your code
1. Delete the template's proto: rm proto/mydata.proto src/pb/mydata.v1.rs (use whatever names the template actually created).

2. Create proto/transfers.proto:


syntax = "proto3";

package transfers.v1;

message Transfers {
  repeated Transfer transfers = 1;
}

message Transfer {
  string from = 1;
  string to = 2;
  uint64 amount = 3;
}
3. Edit substreams.yaml. Change only these four things and keep everything else, including the template's inputs: line:


protobuf:
  files:
    - transfers.proto
...
modules:
  - name: map_transfers
    kind: map
    initialBlock: 385870151
    inputs:
      - ...keep what the template generated...
    output:
      type: proto:transfers.v1.Transfers
4. Add the base58 crate: cargo add bs58

5. Replace all of src/lib.rs:


mod pb;

use pb::transfers::v1::{Transfer, Transfers};
use substreams_solana::pb::sf::solana::r#type::v1::Block;

const SYSTEM_PROGRAM: &str = "11111111111111111111111111111111";

#[substreams::handlers::map]
fn map_transfers(block: Block) -> Result<Transfers, substreams::errors::Error> {
    let mut transfers = Vec::new();

    for trx in block.transactions.iter() {
        let meta = match &trx.meta {
            Some(meta) => meta,
            None => continue,
        };
        // failed transactions never moved any funds
        if meta.err.is_some() {
            continue;
        }
        let message = match trx.transaction.as_ref().and_then(|t| t.message.as_ref()) {
            Some(message) => message,
            None => continue,
        };

        // v0 transactions load extra accounts from address lookup tables
        let mut accounts: Vec<&Vec<u8>> = message.account_keys.iter().collect();
        accounts.extend(meta.loaded_writable_addresses.iter());
        accounts.extend(meta.loaded_readonly_addresses.iter());

        for (i, ix) in message.instructions.iter().enumerate() {
            if let Some(t) = parse_transfer(&accounts, ix.program_id_index, &ix.accounts, &ix.data) {
                transfers.push(t);
            }
            // transfers made by other programs (CPI) appear as inner instructions
            for group in meta.inner_instructions.iter().filter(|g| g.index as usize == i) {
                for inner_ix in group.instructions.iter() {
                    if let Some(t) = parse_transfer(&accounts, inner_ix.program_id_index, &inner_ix.accounts, &inner_ix.data) {
                        transfers.push(t);
                    }
                }
            }
        }
    }

    Ok(Transfers { transfers })
}

fn parse_transfer(accounts: &[&Vec<u8>], program_id_index: u32, ix_accounts: &[u8], data: &[u8]) -> Option<Transfer> {
    let program_id = accounts.get(program_id_index as usize)?;
    if bs58::encode(program_id).into_string() != SYSTEM_PROGRAM || data.len() < 12 {
        return None;
    }

    let instruction_type = u32::from_le_bytes(data[0..4].try_into().ok()?);
    let amount = u64::from_le_bytes(data[4..12].try_into().ok()?);

    // System Program: 2 = Transfer [from, to], 11 = TransferWithSeed [from, base, to]
    let (from_pos, to_pos): (usize, usize) = match instruction_type {
        2 => (0, 1),
        11 => (0, 2),
        _ => return None,
    };

    let from = accounts.get(*ix_accounts.get(from_pos)? as usize)?;
    let to = accounts.get(*ix_accounts.get(to_pos)? as usize)?;

    Some(Transfer {
        from: bs58::encode(from).into_string(),
        to: bs58::encode(to).into_string(),
        amount,
    })
}
If the template's use substreams_solana::...Block; line looks different from mine, keep the template's version.

Step 5: build, run, verify

substreams build
ls *.spkg
substreams run -e mainnet.sol.streamingfast.io:443 solana-transfers-v0.1.0.spkg map_transfers -s 385870151 -t +6 -o jsonl > raw_output.jsonl
Use the actual .spkg filename from ls. -t +6 gives 6 blocks because the stop block is exclusive.

Convert to the required format:


jq -c '.["@data"].transfers[]? | {from, to, amount: ((.amount // "0") | tonumber)}' raw_output.jsonl > transfers.jsonl
Protobuf's JSON encoding outputs uint64 as a string; tonumber turns it into the required integer. Put that reasoning in the README, because it shows you understood the format.

Check the results:


jq -c '{block: .["@block"], count: ((.["@data"].transfers // []) | length)}' raw_output.jsonl
wc -l transfers.jsonl
grep Eq1c3uNugn3FRpJ99K2q1ZyQrora3jntUqvkMnGroKkB transfers.jsonl
The first command lists blocks 151–156 with a transfer count for each. A missing slot just means Solana skipped it.
If the grep finds their example with 325253, your interpretation is confirmed. If it doesn't, tell me: it would mean they also count SPL token transfers, and I'll add that.
Step 6: README, push, submit
Cover these in README.md:

What it does
Design decisions: the 4 scope points above, plus the uint64-as-string reasoning
How to run: the commands above
Results: transfers per block, and whether the example matched
Challenges: your error notes
How I used AI
Next steps: SPL tokens, the transaction signature in the output, tests
Then commit:


git init
git add .
git status
git commit -m "Solana SOL transfers Substreams module"
Check the git status output: .substreams.env must not be listed. Push to a new GitHub repo, then submit the repo link and the .spkg.

Send me any error exactly as it appears and we'll fix it.











