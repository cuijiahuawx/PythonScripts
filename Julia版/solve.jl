using Parsers

mutable struct Work
    ES; EF; LS; LF; TF; FF; prework; work; time; nexwork;
    function Work(info)
        ES, EF ,LS , LF, TF, FF = [0 for i in 1:6]
        prework, work, time, nexwork = split(info, '-')
        time = Parsers.parse(Int, time)
        new(ES, EF ,LS , LF, TF, FF, prework, work, time, nexwork)
    end
end

mutable struct Network
    dict; index; reverseindex; endtag; calculatime;
    function Network(question, plane="no")
        dict = Dict()
        index = []
        reverseindex = []
        endtag = []
        for i in question
            w = Work(i)
            if w.nexwork == "empty"
                push!(endtag, w.work)
            end
            dict[split(i, '-')[2]] = w
            push!(index, split(i, '-')[2])
            reverseindex = reverse(index)
        end
        # ES, EF
        for i in index
            work = dict[i]
            pretag = work.prework
            if pretag == "empty"
            elseif length(pretag) == 1
                work.ES = dict[work.prework].EF
            else
                work.ES = maximum([dict[string(i)].EF for i in work.prework])
            end
            work.EF = work.ES + work.time
        end
        # LS, LF
        for i in reverseindex
            work = dict[i]
            nextag = work.nexwork
            if nextag == "empty"
                global calculatime = maximum([dict[i].EF for i in endtag])
                if plane == "no"
                    work.LF = calculatime
                else
                    work.LF = Parsers.parse(Int, plane)
                end
            elseif length(nextag) == 1
                work.LF = dict[nextag].LS
            else
                work.LF = minimum([dict[string(i)].LS for i in nextag])
            end
            work.LS = work.LF - work.time
        end
        # TF
        for i in index
            work = dict[i]
            work.TF = work.LS - work.ES
        end
        # FF
        for i in reverseindex
            work = dict[i]
            nextag = work.nexwork
            endvalue = maximum(dict[i].LF for i in endtag)
            if nextag == "empty"
                work.FF = endvalue - work.EF
            elseif length(nextag) == 1
                work.FF = dict[nextag].ES - work.EF
            else
                work.FF = minimum([dict[string(i)].ES for i in nextag]) - work.EF
            end
        end
        new(dict, index, reverseindex, endtag, calculatime)
    end
end

question =
"
empty-a-10-bcd
a-b-10-e
a-c-20-f
a-d-30-g
b-e-20-h
c-f-20-hi
d-g-30-i
fg-i-50-j
ef-h-30-j
hi-j-10-empty
"
function network(question)
    question = split(question)
    if occursin("-", question[end])
        network = Network(question)
    else
        network = Network(question[1:end-1], question[end])
    end
    network
end

function show(network::Network)
    for i in network.index
        v = network.dict[i]
        println(
"$(v.work):
------
$(v.ES),$(v.LS),$(v.TF)
$(v.EF),$(v.LF),$(v.FF)
------"
)
    end
end

show(network(question))
