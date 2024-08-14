from amaranth.sim import Simulator
from hw_encoder import COBSEncoder
from sw_encoder import cobs_encode

test_cases = [
    [11, 22, 33, 44],
    [11, 22, 0, 33],
    [0, 11, 0],
    [0],
    [11, 00, 00, 00]
]

async def testbench(ctx, data):
    await ctx.tick()
    await ctx.tick()

    # Fill encoder with data to encode
    ctx.set(dut.data_in_valid, True)
    for d in data:
        ctx.set(dut.data_in, d)
        await ctx.tick()

    ctx.set(dut.data_in_valid, False)

    # for i in range(len(data)):
        # print(ctx.get(dut.memory.data[i]))


    # Start encoding
    ctx.set(dut.start, True)
    await ctx.tick()
    ctx.set(dut.start, False)

    # Capture output
    output = []
    for _ in range(25):
        if ctx.get(dut.data_out_valid):
            output.append(ctx.get(dut.data_out))

        await ctx.tick()

    expected = cobs_encode(data)
    print(f"input   : {data}")
    print(f"from HDL: {output}")
    print(f"expected: {expected}")
    print(f"match: {output == expected}")
    print()



for i, case in enumerate(test_cases):
    dut = COBSEncoder()
    sim = Simulator(dut)
    sim.add_clock(1e-6)

    async def testbench_wrapper(ctx):
        return await testbench(ctx, case)

    sim.add_testbench(testbench_wrapper)
    with sim.write_vcd(f"encoder_case{i}.vcd"):
        sim.run()