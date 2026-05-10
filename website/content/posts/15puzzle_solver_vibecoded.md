--- title: "Optimal 15 puzzle solver" date: 2026-05-10 tags: ["rust",
"puzzle", "solver"] draft: true ---

Since I was young I always enjoyed puzzles, at two levels: 1) Solving them
myself, and 2) Writing code to solve them. It is a two in one. Take the Rubik's
cube as an example. Solving it as a human requires memorizing multiple
algorithms and knowing when to use them. To solve it faster, you memorize more
algorithms for more cases. You improve your pattern recognition. Your finger
dexterity. When solving as a computer, you don't use "cube algorithms",
instead, classical search algorithms are used, such as a Depth First Search, or
an Iterative Deepening. Even a bad algorithm, assuming you have enough time, will
solve the Cube. The fun is in solving it as fast as possible. Here there are
two approaches: 1) Improving the search heuristics, like using group theory and
removing redundant symmetric cases, and 2) Optimizing the code itself, like
precomputing move tables.

So far my most complex project has been
[cubotron](https://github.com/h3nnn4n/cubotron), which was written in the pre
LLM era. By now I have done some small optimizations using an LLM, but the bulk
was written by hand, and a significant time was spent just on debugging. It was
extremely fun and rewarding and it took a long time to be decently fast. Now,
with the widespread use and availability of Coding Agents, and kernel
vulnerabilities being found autonomously and functional compilers being written
from scratch without human input, I got curious with a possibility of writing a
puzzle solver without doing a single line of code. This would remove the fun of
writing the code and debugging and all the pride in the craftsmanship. But in
exchange it would allow to focus exclusively in the thinking process on how to
make it faster. At least that was the theory.

For this project, I decided to solve the
[15 puzzle](https://en.wikipedia.org/wiki/15_puzzle). It is a simple
combinatorial puzzle, that is NP-Hard. A brute force search won't be able to
solve a significant number of cases. Something smarter like IDA* can take care
of a decent chunk of the possible scrambles. To solve all scrambles reliably
and under a few seconds, several optimizations are required.

Along with making the solver, I was also interested in the difference between
agents and models. So I tried a selfhosted qwen3-32b with
[swival](https://swival.dev/), which is supposed to be an agent optimized for
self hosted models with a small context. Then, next I used MiniMax M2.5 with
[opencode](https://opencode.ai/). Finally, I used Claude Code with Open 3.7, 1M
context with a high effort.

All 3 agents started on a rust implementation and had similar prompts where
possible, but this quickly became infeasible as they started to drift approach.
The self-hosted version quickly became stuck when implementing the data
representation for the board and couldn't even make the files compile. After
some time I gave up because it wasn't going anywhere. With opencode, the data
structure representing the board was completely broken and it required a lot of
hand holding to fix it. Then, it got to a functional solver using IDA*, but it
was extremely slow. At this point it was constantly getting lost and becoming
stuck. Then I gave up on it.

With Claude Code, as expected of a commercial product using one of the most
advanced coding models available, the implementation went very smoothly. In
fact, I had to tell claude to stop helping me and only do the optimizations I
told, and nothing else. The board data structure was trivial. The initial IDA*
solver was effortless. From there I added a simple benchmarking platform, using
some hard scrambles from a paper from 1985. Then I started to brainstorm and
test multiple hypotheses. With the agent it was extremely easy to test new
approaches. It built caches for removing the cost of computing transposition
tables and pattern databases. Added multithreading to precompute things faster,
and with a simple prompt it could implement multiple variants of a heuristic,
evaluate and tell me which one was the easiest.

This was a very interesting experience, and the first time I have "vibe coded"
something from scratch. Since this was something way more complex than a SaaS
project, it was actually fun. It was like being a professor and guiding
students and technicians on a research project. It replaces the fun of writing
the code, with the fun of thinking how to make it faster. The iteration loop
for thinking of new ways to optimize was significantly reduced, where I could
do a pretty respectable solver in an afternoon. My previous rubiks cube
solver took weeks / month to get to where it is now.

Fun/sad story: When working, I have the Company's API key for claude code and I
can use it without having to worry with costs. For this project I was using my
personal account, and since I was so used to not caring about how much I was
spending I just kept "coding". When the project was 95% I stopped to read
emails while it crunched a bunch of numbers, and then I saw multiple emails
about running out of balance and it being automatically refilled. I spent $380
in an afternoon vibecoding something. Here where I live this is the 70th
percentile for per capita income in the poorest states.
