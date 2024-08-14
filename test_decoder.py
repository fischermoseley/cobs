from amaranth.sim import Simulator
from hw_decoder import COBSDecoder

test_cases = [
    [0, 5, 11, 22, 33, 44, 0, 5, 11, 22, 33, 44, 0],
    [0, 1, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 2, 11, 1, 1, 1, 0]
]

async def testbench(ctx, data):
    await ctx.tick()
    await ctx.tick()


    output = []

    ctx.set(dut.data_in_valid, True)
    for d in data:
        ctx.set(dut.data_in, d)


        # Capture output
        if ctx.get(dut.data_out_valid):
            output.append(ctx.get(dut.data_out))


        await ctx.tick()

    ctx.set(dut.data_in_valid, False)
    await ctx.tick()

    print(output)

    # expected = cobs_encode(data)
    # print(f"input   : {data}")
    # print(f"from HDL: {output}")
    # print(f"expected: {expected}")
    # print(f"match: {output == expected}")
    # print()



for i, case in enumerate(test_cases):
    dut = COBSDecoder()
    sim = Simulator(dut)
    sim.add_clock(1e-6)

    async def testbench_wrapper(ctx):
        return await testbench(ctx, case)

    sim.add_testbench(testbench_wrapper)
    with sim.write_vcd(f"decoder_case{i}.vcd"):
        sim.run()